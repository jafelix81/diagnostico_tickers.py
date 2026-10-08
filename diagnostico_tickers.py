import yfinance as yf
import pandas as pd
import time

TICKERS = ["AVB", "EA", "EQR", "LPRO", "WBD", "WBS"]


def analizar_data(data, ticker, fuente):
    print("\n" + "=" * 70)
    print(f"TICKER: {ticker} | FUENTE: {fuente}")
    print("=" * 70)

    if data is None:
        print("DATA = None")
        return

    print(f"Tipo: {type(data)}")
    print(f"Shape: {data.shape}")
    print(f"Columnas: {data.columns}")

    if data.empty:
        print("RESULTADO: DATAFRAME VACÍO")
        return

    # ---------------------------------------------------------
    # Detectar columna Close
    # ---------------------------------------------------------
    close = None

    try:
        if isinstance(data.columns, pd.MultiIndex):
            if "Close" in data.columns.get_level_values(0):
                close = data["Close"]
                if isinstance(close, pd.DataFrame):
                    if ticker in close.columns:
                        close = close[ticker]
                    elif len(close.columns) == 1:
                        close = close.iloc[:, 0]

        else:
            if "Close" in data.columns:
                close = data["Close"]

    except Exception as e:
        print(f"Error obteniendo Close: {e}")

    if close is None:
        print("RESULTADO: NO SE ENCONTRÓ COLUMNA CLOSE")
        return

    close = pd.to_numeric(close, errors="coerce").dropna()

    print(f"Observaciones Close válidas: {len(close)}")

    if len(close) > 0:
        print(f"Primera fecha: {close.index.min()}")
        print(f"Última fecha:  {close.index.max()}")
        print(f"Primer Close: {close.iloc[0]}")
        print(f"Último Close:  {close.iloc[-1]}")

    if len(close) >= 260:
        print(">>> RESULTADO: OK - suficientes observaciones")
    else:
        print(">>> RESULTADO: INSUFICIENTE - menos de 260")


# ============================================================
# 1. BULK DOWNLOAD 10Y
# ============================================================

print("\n")
print("#" * 80)
print("DIAGNÓSTICO CERE — TICKERS PROBLEMÁTICOS")
print("#" * 80)

print("\n1) DESCARGA BULK 10Y")

try:
    bulk = yf.download(
        TICKERS,
        period="10y",
        interval="1d",
        auto_adjust=False,
        progress=False,
        threads=False,
        group_by="column"
    )

    print(f"\nBulk general:")
    print(f"Shape: {bulk.shape}")
    print(f"Columnas: {bulk.columns}")

except Exception as e:
    print(f"ERROR BULK: {e}")
    bulk = None


if bulk is not None and not bulk.empty:

    for ticker in TICKERS:

        try:

            if isinstance(bulk.columns, pd.MultiIndex):

                # Estructura habitual:
                # Close / Ticker
                if ticker in bulk.columns.get_level_values(1):
                    ticker_data = bulk.xs(
                        ticker,
                        axis=1,
                        level=1,
                        drop_level=True
                    )

                else:
                    print(f"\n{ticker}: no aparece en nivel 1 del MultiIndex")
                    continue

            else:
                ticker_data = bulk.copy()

            analizar_data(
                ticker_data,
                ticker,
                "BULK 10Y"
            )

        except Exception as e:
            print(f"\n{ticker}: ERROR procesando bulk: {e}")


# ============================================================
# 2. INDIVIDUAL TICKER.history() 10Y
# ============================================================

print("\n\n")
print("#" * 80)
print("2) DESCARGA INDIVIDUAL — Ticker.history() — 10Y")
print("#" * 80)

for ticker in TICKERS:

    print(f"\nDescargando individual: {ticker}")

    try:

        stock = yf.Ticker(ticker)

        data = stock.history(
            period="10y",
            interval="1d",
            auto_adjust=False
        )

        analizar_data(
            data,
            ticker,
            "INDIVIDUAL history() 10Y"
        )

    except Exception as e:

        print(f"{ticker}: ERROR individual: {e}")

    time.sleep(1)


# ============================================================
# 3. INDIVIDUAL 5Y
# ============================================================

print("\n\n")
print("#" * 80)
print("3) DESCARGA INDIVIDUAL — 5Y")
print("#" * 80)

for ticker in TICKERS:

    print(f"\nDescargando 5Y: {ticker}")

    try:

        stock = yf.Ticker(ticker)

        data = stock.history(
            period="5y",
            interval="1d",
            auto_adjust=False
        )

        analizar_data(
            data,
            ticker,
            "INDIVIDUAL history() 5Y"
        )

    except Exception as e:

        print(f"{ticker}: ERROR 5Y: {e}")

    time.sleep(1)


# ============================================================
# 4. MAX
# ============================================================

print("\n\n")
print("#" * 80)
print("4) DESCARGA INDIVIDUAL — MAX")
print("#" * 80)

for ticker in TICKERS:

    print(f"\nDescargando MAX: {ticker}")

    try:

        stock = yf.Ticker(ticker)

        data = stock.history(
            period="max",
            interval="1d",
            auto_adjust=False
        )

        analizar_data(
            data,
            ticker,
            "INDIVIDUAL history() MAX"
        )

    except Exception as e:

        print(f"{ticker}: ERROR MAX: {e}")

    time.sleep(1)


print("\n\n")
print("#" * 80)
print("FIN DEL DIAGNÓSTICO")
print("#" * 80)
