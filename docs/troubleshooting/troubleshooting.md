# Troubleshooting

This guide helps you resolve common issues you might encounter while using Sidekick.

## Common Issues and Solutions

### 1. Ollama Connection Issues

**Problem**: Unable to connect to Ollama

**Solutions**:
1. Ensure Ollama is running in the background
2. Verify the Ollama host URL in your `.env` file
3. Check if Ollama is running on the correct port (default: 11434)
4. Restart Ollama service

### 2. Model Installation Issues

**Problem**: Model fails to install or load

**Solutions**:
1. Verify your model is properly installed:
   ```bash
   ollama list
   ```
2. Check available disk space
3. Try pulling the model again:
   ```bash
   ollama pull your-model-name
   ```
4. Ensure your system meets the model's requirements

### 3. Application Won't Start

**Problem**: Sidekick fails to launch

**Solutions**:
1. Check Python version (3.10+ required)
2. Verify all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```
3. Check the `.env` file configuration
4. Look for error messages in the console

### 4. Performance Issues

**Problem**: Slow responses or high resource usage

**Solutions**:
1. Try a smaller model
2. Close unnecessary applications
3. Check system resources
4. Verify no other processes are competing for GPU resources

## Getting Help

If you're still experiencing issues:

1. Check the [documentation](https://github.com/raythurman2386/sidekick)
2. Open an [issue on GitHub](https://github.com/raythurman2386/sidekick/issues)
3. Include relevant information:
   - Error messages
   - System specifications
   - Steps to reproduce the issue
   - Logs (if available)
