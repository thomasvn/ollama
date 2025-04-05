#!/bin/bash

if ! pgrep -x "ollama" > /dev/null; then
    echo "❌ Ollama not running. Run 'ollama serve' to start"
    exit 1
fi

conversation="OS: macOS\nTask: $1"
echo "🤖 CLI Assistant | Type question or 'exit'"

while true; do
    read -p "> " user_input
    
    if [ "$user_input" = "exit" ]; then
        echo "👋 Done"
        break
    fi
    
    conversation="$conversation\nUser: $user_input"
    echo "⚡ Processing..."
    cmd=$(ollama run qwen2.5-coder "$conversation\nProvide only the exact command to execute (no markdown, no explanations, no backticks):")
    echo "$ $cmd"
    echo "Run? (y/n)"
    read -r answer
    
    if [ "$answer" = "y" ]; then
        output=$(eval "$cmd" 2>&1)
        echo -e "\nOutput:"
        echo "$output"
        conversation="$conversation\nAssistant: I executed: $cmd\nOutput: $output"
    fi
done
