# Lean Engine Dockerfile
# This builds the QuantConnect Lean algorithmic trading engine

FROM quantconnect/lean:foundation

WORKDIR /Lean

# Copy the Lean engine source
COPY ./Lean /Lean

# Install Python debugging tools
RUN pip install --no-cache-dir debugpy ptvsd pydevd-pycharm

# Set working directory to launcher
WORKDIR /Lean/Launcher/bin/Debug

# Entry point for Lean engine
ENTRYPOINT [ "dotnet", "QuantConnect.Lean.Launcher.dll" ]
