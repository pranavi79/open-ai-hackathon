#!/bin/bash

echo "[START] Emergency Response System - SAFE DEMO MODE"
echo "============================================================"

# Ensure demo mode is enabled
echo "[SECURITY] Enabling demo mode for safe testing..."
python cost_protection_cli.py demo-on

echo ""
echo "[OK] Demo mode enabled - No API charges will occur!"
echo "[INFO] All functionality works perfectly in demo mode"
echo "[DEMO] Perfect for hackathon presentation!"
echo ""

# Start the server
echo "[SERVER] Starting FastAPI server..."
cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"🚀 Starting Emergency Response System - SAFE DEMO MODE"
echo "=" * 60

# Ensure demo mode is enabled
echo "🛡️  Enabling demo mode for safe testing..."
python cost_protection_cli.py demo-on

echo ""
echo "✅ Demo mode enabled - No API charges will occur!"
echo "� All functionality works perfectly in demo mode"
echo "🎯 Perfect for hackathon presentation!"
echo ""

# Start the server
echo "🌟 Starting FastAPI server..."
cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
