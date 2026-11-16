#!/bin/sh
# Swipe Purge: carrega as chaves do admin e roda o comando original do servico.
eval "$(python3 /MoneyPrinterTurbo/swipe/buscar_chaves.py)"
exec "$@"
