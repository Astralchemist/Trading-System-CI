# Lean Engine Dockerfile
# This builds the QuantConnect Lean algorithmic trading engine

FROM quantconnect/lean:foundation

WORKDIR /Lean

# Copy the Lean engine source
COPY ./Lean /Lean

# Install Python debugging tools
RUN pip install --no-cache-dir debugpy ptvsd pydevd-pycharm

# Restore NuGet packages and build the Lean engine
RUN dotnet restore /Lean/QuantConnect.Lean.sln && \
    dotnet build /Lean/QuantConnect.Lean.sln -c Release --no-restore

# Verify the DLL exists and list the output directory
RUN ls -la /Lean/Launcher/bin/Release/ || echo "Build output not found"

# Entry point for Lean engine - run from /Lean root with explicit path
WORKDIR /Lean
ENTRYPOINT [ "dotnet", "/Lean/Launcher/bin/Release/QuantConnect.Lean.Launcher.dll" ]
