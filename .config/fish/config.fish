# https://fishshell.com/docs/current/interactive.html#vi-mode-commands

if status is-interactive
    # Commands to run in interactive sessions can go here
    function fish_hybrid_key_bindings --description \
        "Vi-style bindings that inherit emacs-style bindings in all modes"
        for mode in default insert visual
            fish_default_key_bindings -M $mode
        end
        fish_vi_key_bindings --no-erase
    end
    set -g fish_key_bindings fish_hybrid_key_bindings
end
