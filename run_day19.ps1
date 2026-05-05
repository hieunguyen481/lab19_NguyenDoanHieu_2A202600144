param(
    [ValidateSet("offline", "openai-generate", "openai-extract", "neo4j-export")]
    [string]$Mode = "offline"
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if ($Mode -eq "offline") {
    Remove-Item Env:\USE_LLM_EXTRACTION -ErrorAction SilentlyContinue
    python -B src/pipeline.py
    exit $LASTEXITCODE
}

if ($Mode -eq "openai-generate") {
    Remove-Item Env:\USE_LLM_EXTRACTION -ErrorAction SilentlyContinue
    python -B src/pipeline.py
    exit $LASTEXITCODE
}

if ($Mode -eq "openai-extract") {
    $env:USE_LLM_EXTRACTION = "1"
    python -B src/pipeline.py
    exit $LASTEXITCODE
}

if ($Mode -eq "neo4j-export") {
    python -B src/pipeline.py
    python -B src/export_neo4j.py
    exit $LASTEXITCODE
}
