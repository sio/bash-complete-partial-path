#!/usr/bin/env bash
#
# Zsh-like expansion of incomplete file paths for Bash.
# Source this file from your ~/.bashrc and use `_bcpp --defaults`
# to enable the described behavior.
#
# Example: `/u/s/a<Tab>` will be expanded into `/usr/share/applications`
#
# https://github.com/sio/bash-complete-partial-path
#


# Copyright 2018 Vitaly Potyarkin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


#
# Detect sed binary once at load time
#
_bcpp_sed_detect() {
    local SED GNU_SED
    SED="sed"
    GNU_SED="gsed" # macOS ships BSD sed by default, gnu-sed has to be installed with brew
    if [[ $OSTYPE == darwin* ]]
    then
        if type "$GNU_SED" &> /dev/null
        then
            SED="$GNU_SED"
        else
            echo "Completion script requires GNU sed, please install it with brew" >&2
        fi
    fi
    echo "$SED"
}
_BCPP_SED=$(_bcpp_sed_detect)


#
# Take a single incomplete path and fill it with wildcards
# e.g. /u/s/app/ -> /u*/s*/app*
#
_bcpp_put_wildcards() {
    local PROCESSED TILDE_EXPANSION INPUT

    INPUT="$@"
    PROCESSED=$( \
        echo "$INPUT" | \
        $_BCPP_SED \
            -e 's:\([^\*\~]\)/:\1*/:g' \
            -e 's:\([^\/\*]\)$:\1*:g' \
            -e 's:^\(\~[^\/]*\)\*\/:\1/:' \
            -Ee 's:(\.+)\*/:\1/:g' \
    )
    eval "TILDE_EXPANSION=$(printf '%q' "$PROCESSED"|$_BCPP_SED -e 's:^\\\~:~:g')"

    # Workaround for Mingw pseudo directories for drives,
    # i.e. `/c/` refers to drive `C:\`, but glob `/c*/` returns no matches
    if [[ "$INPUT" =~ ^\/[a-zA-Z]\/.* && -d "${INPUT::2}" ]]
    then
        TILDE_EXPANSION="${TILDE_EXPANSION::2}${TILDE_EXPANSION:3}"
    fi

    echo "$TILDE_EXPANSION"
}


#
# Bash completion function for expanding partial paths
#
# This is a generic worker. It accepts 'file' or 'directory' as the first
# argument to specify desired completion behavior
#
_bcpp_complete() {
    local WILDCARDS ACTION LINE OPTION INPUT UNQUOTED_INPUT QUOTE

    ACTION="$1"
    if [[ "_$1" == "_-d" ]]
    then  # _filedir compatibility
        ACTION="directory"
    fi
    if [[ "$COMP_CWORD" -ge 0 ]]
    then
        INPUT="${COMP_WORDS[$COMP_CWORD]}"
    else
        INPUT=""
    fi

    # Detect and strip opened quotes
    if [[ "${INPUT:0:1}" == "'" || "${INPUT:0:1}" == '"' ]]
    then
        QUOTE="${INPUT:0:1}"
        INPUT="${INPUT:1}"
    else
        QUOTE=""
    fi

    # Prepare the reply
    COMPREPLY=()
    compopt -o nospace
    compopt -o bashdefault
    compopt -o default

    # If input is already a valid path, do not try to be clever
    if [[ -e "$INPUT" ]]
    then
        if [[ "_$ACTION" == "_directory" ]]
        then
            OPTION="dirnames"
        else
            OPTION="filenames"
        fi
        COMPREPLY=($(compgen -o "$OPTION" "$INPUT"))
        return
    fi

    # Add wildcards to each path element
    WILDCARDS=$(_bcpp_put_wildcards "$INPUT")

    # Collect completion options
    while read -r -d $'\n' LINE
    do
        if [[ "_$ACTION" == "_directory" && ! -d "$LINE" ]]
        then  # skip non-directory paths when looking for directory
            continue
        fi
        if [[ -z "$LINE" ]]
        then  # skip empty suggestions
            continue
        fi
        if [[ -z "$QUOTE"  ]]
        then  # escape special characters unless user has opened a quote
            LINE=$(printf "%q" "$LINE")
        fi
        COMPREPLY+=("$LINE")
    done <<< $(compgen -G "$WILDCARDS" "$WILDCARDS" 2>/dev/null)
    return 0  # do not clutter $? value (last exit code)
}


# Wrappers
_bcpp_complete_dir() { _bcpp_complete directory; }
_bcpp_complete_file() { _bcpp_complete file; }


# Manage enhanced path completion
_bcpp() {
    local DEFAULT ALL KEYS ARG USAGE UNKNOWN

    DEFAULT="--files --dirs --override --nocase --readline"
    ALL="--files --dirs --override --nocase --readline"
    USAGE=(
        "Usage: $FUNCNAME OPTIONS"
        "    Manage enhanced path completion in bash"
        ""
        "Options:"
        "    --defaults"
        "        Enable the subset of features recommended by maintainer."
        "        Currently equals to:"
        "        \"$DEFAULT\""
        "    --all"
        "        Enable all optional features. Equals to:"
        "        \"$ALL\""
        "    --help"
        "        Show this help message"
        ""
        "Individual feature flags:"
        "    --files"
        "        Enable enhanced completion for file paths"
        "    --dirs"
        "        Complete \`cd\` with paths to directories only"
        "    --override"
        "        Override bash-completion if it's in use"
        "    --nocase"
        "        Make path completion case insensitive"
        "    --readline"
        "        Configure readline for better user experience. Equals to:"
        "        \"--readline-menu --readline-color --readline-misc\""
        "    --readline-color"
        "        Enable colors in completion"
        "    --readline-menu"
        "        Use \`menu-complete\` when TAB key is pressed instead of default"
        "        \`complete\`"
        "    --readline-misc"
        "        Other useful readline tweaks"
        ""
        "Copyright 2018 Vitaly Potyarkin"
        "<https://github.com/sio/bash-complete-partial-path>"
        ""
        "This program is Free Software and comes with ABSOLUTELY NO WARRANTY,"
        "to the extent permitted by applicable law. For more information see:"
        "<http://www.apache.org/licenses/LICENSE-2.0>"
    )

    # Modify selected features list
    for ARG in "$@"
    do
        case "$ARG" in
            --defaults)
                set -- "$@" $DEFAULT ;;
            --all)
                set -- "$@" $ALL ;;
        esac
    done

    # Detect selected features
    KEYS=""
    for ARG in "$@"
    do
        case "$ARG" in
            --files)
                KEYS="${KEYS}f" ;;
            --dirs)
                KEYS="${KEYS}d" ;;
            --override)
                KEYS="${KEYS}o" ;;
            --nocase)
                KEYS="${KEYS}c" ;;
            --readline)
                KEYS="${KEYS}mlr" ;;
            --readline-menu)
                KEYS="${KEYS}m" ;;
            --readline-color)
                KEYS="${KEYS}l" ;;
            --readline-misc)
                KEYS="${KEYS}r" ;;
            --help|--usage|-h)
                KEYS="${KEYS}H" ;;
            --defaults|--all)
                ;;
            *)
                KEYS="${KEYS}U"
                UNKNOWN+=("$ARG")
                ;;
        esac
    done

    # Special cases that terminate function
    if [[ "$KEYS" == *H* || -z "$@" ]]  # --help|--usage|-h
    then
        printf "%s\n" "${USAGE[@]}"
        return 0
    fi
    if [[ "$KEYS" == *U* ]]  # unknown arguments
    then
        echo -e \
            "Unknown arguments: ${UNKNOWN[@]}" \
            "\nRefer to \`$FUNCNAME --help\` for more information" \
            >&2
        return 1
    fi

    # Enable selected functionality. The order of execution does not depend on
    # the order of command line parameters
    if [[ "$KEYS" == *f* ]]  # --files
    then
        complete -o bashdefault -o default -o nospace -D -F _bcpp_complete_file
    fi
    if [[ "$KEYS" == *d* ]]  # --dirs
    then
        complete -o bashdefault -o default -o nospace -F _bcpp_complete_dir cd
    fi
    if [[ "$KEYS" == *o* ]]  # --override
    then
        _bcpp_filedir_original_code=$(declare -f _filedir|tail -n+2)
        if [[ ! -z "$_bcpp_filedir_original_code" ]]
        then
            type _bcpp_filedir_original &>/dev/null || \
                eval "_bcpp_filedir_original() $_bcpp_filedir_original_code"
            _filedir() {
                _bcpp_filedir_original "$@"
                _bcpp_complete "$@"
            }
        fi
        _bcpp_filedir_xspec_original_code=$(declare -f _filedir_xspec|tail -n+2)
        if [[ ! -z "$_bcpp_filedir_xspec_original_code" ]]
        then
            type _bcpp_filedir_xspec_original &>/dev/null || \
                eval "_bcpp_filedir_xspec_original() $_bcpp_filedir_xspec_original_code"
            _filedir_xspec() {
                _bcpp_filedir_xspec_original "$@"
                _bcpp_complete "$@"
            }
        fi
    fi
    if [[ "$KEYS" == *c* ]]  # --nocase
    then
        shopt -s nocaseglob
        bind 'set completion-ignore-case on'
    fi
    if [[ "$KEYS" == *m* ]]  # --readline-menu
    then
        bind 'TAB:menu-complete'
        bind 'set menu-complete-display-prefix on'
    fi
    if [[ "$KEYS" == *l* ]]  # --readline-color
    then
        bind 'set colored-completion-prefix on'
        bind 'set colored-stats on'
    fi
    if [[ "$KEYS" == *r* ]]  # --readline-misc
    then
        bind 'set show-all-if-ambiguous on'
        bind 'set show-all-if-unmodified on'
    fi
}
