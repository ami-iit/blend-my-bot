#!/usr/bin/env bash
#
# Usage: sudo ./setup_conda_blender.sh /usr/share/blender/4.1
# ------------------------------------------------------------------------------

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <BLENDER_ROOT>"
  exit 1
fi

BLENDER_ROOT="$(realpath "$1")"
PYTHON_DIR="$BLENDER_ROOT/python"

# ──────────────────────────────────────────────────────────────────────────────
# 1. Locate Blender’s bundled Python binary, whatever it’s called
# ──────────────────────────────────────────────────────────────────────────────
BLENDER_PY_BIN="$(find "$PYTHON_DIR/bin" -maxdepth 1 -type f -executable -name 'python3*' | head -n1 || true)"

if [[ -z "$BLENDER_PY_BIN" ]]; then
  echo "❌  Cannot find Blender's bundled Python inside: $PYTHON_DIR/bin/" >&2
  exit 1
fi

# Pull out the major.minor version (e.g. 3.11)
BLENDER_PY_VERSION="$("$BLENDER_PY_BIN" - <<'PY'
import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")
PY
)"
echo "→ Blender uses Python $BLENDER_PY_VERSION"

# ──────────────────────────────────────────────────────────────────────────────
# 2. Create / reuse matching Conda environment
# ──────────────────────────────────────────────────────────────────────────────
ENV_NAME="blender_env_${BLENDER_PY_VERSION//./}"   # e.g. blender_env311
CONDA_HOME="$(conda info --base)"
ENV_PATH="$CONDA_HOME/envs/$ENV_NAME"

if conda env list | grep -qE "^$ENV_NAME\s"; then
  echo "✓ Conda env '$ENV_NAME' already exists"
else
  echo "→ Creating Conda env '$ENV_NAME' with python=$BLENDER_PY_VERSION"
  conda create -y -n "$ENV_NAME" python="$BLENDER_PY_VERSION"
fi

# ──────────────────────────────────────────────────────────────────────────────
# 3. Swap Blender’s python/ with a symlink to the env
# ──────────────────────────────────────────────────────────────────────────────
cd "$BLENDER_ROOT"

if [[ ! -L python ]]; then
  TS=$(date +%s)
  sudo mv python "python.bak.$TS"
  echo "→ Backed up original python/ to python.bak.$TS"
fi

sudo ln -sfn "$ENV_PATH" python   # -f/-n: replace if link already exists
echo "✓ Linked $ENV_PATH  →  $BLENDER_ROOT/python"

echo
echo "All set!  Launch Blender and run in the console:"
echo "    import sys, numpy, pandas, bpy"
echo "    print(sys.executable)"
echo
echo "to verify that it's using your new Conda environment."
