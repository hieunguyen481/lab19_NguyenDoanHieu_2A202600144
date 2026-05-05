param(
    [ValidateSet("offline", "openai-generate", "openai-extract", "neo4j-export", "neo4j-import")]
    [string]$Mode = "offline"
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if ($Mode -eq "offline") {
    $env:USE_OPENAI_GENERATION = "0"
    Remove-Item Env:\USE_LLM_EXTRACTION -ErrorAction SilentlyContinue
    python -B src/pipeline.py
    exit $LASTEXITCODE
}

if ($Mode -eq "openai-generate") {
    $env:USE_OPENAI_GENERATION = "1"
    Remove-Item Env:\USE_LLM_EXTRACTION -ErrorAction SilentlyContinue
    python -B src/pipeline.py
    exit $LASTEXITCODE
}

if ($Mode -eq "openai-extract") {
    $env:USE_OPENAI_GENERATION = "1"
    $env:USE_LLM_EXTRACTION = "1"
    python -B src/pipeline.py
    exit $LASTEXITCODE
}

if ($Mode -eq "neo4j-export") {
    python -B src/pipeline.py
    python -B src/export_neo4j.py
    exit $LASTEXITCODE
}

if ($Mode -eq "neo4j-import") {
    python -B src/pipeline.py
    python -B src/export_neo4j.py
    python -B src/import_neo4j.py
    exit $LASTEXITCODE
}
