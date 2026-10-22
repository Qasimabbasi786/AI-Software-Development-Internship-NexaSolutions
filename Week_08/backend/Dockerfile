# Multi-stage build for ASP.NET Core 8 Web API
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy project file and restore dependencies separately to leverage Docker layer caching
COPY libraryAPI.csproj .
RUN dotnet restore libraryAPI.csproj

# Copy entire backend source and build Release binary
COPY . .
RUN dotnet publish libraryAPI.csproj -c Release -o /app/publish /p:UseAppHost=false

# Runtime image (ASP.NET 8.0 Alpine/Debian minimal image)
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app

# Copy compiled artifacts from build stage
COPY --from=build /app/publish .

# Expose Kestrel port
ENV ASPNETCORE_HTTP_PORTS=8080
ENV ASPNETCORE_ENVIRONMENT=Production

# Run container as non-root user for security hardening
USER $APP_UID

ENTRYPOINT ["dotnet", "libraryAPI.dll"]
