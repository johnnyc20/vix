"""
Connects to your Robinhood account and prints a read-only account summary.

Run this yourself, from your own terminal:

    pip install robin_stocks
    python robinhood_connect.py

You will be prompted for your Robinhood username/email and password
(the password is hidden as you type - it is never shown, printed, or
saved anywhere by this script). If your account has two-factor
authentication turned on, robin_stocks will prompt you for the code
it texts or shows you.

This script only READS data (account info, positions, portfolio value).
It never places, cancels, or modifies any order.
"""

import getpass
import sys

import robin_stocks.robinhood as rh


def connect():
    username = input("Robinhood username/email: ").strip()
    password = getpass.getpass("Robinhood password (hidden): ")

    try:
        login_info = rh.login(username, password)
    except Exception as exc:
        print(f"Login failed: {exc}")
        sys.exit(1)

    if not login_info:
        print("Login failed. Check your username/password and try again.")
        sys.exit(1)

    print("\nConnected to Robinhood.\n")
    return login_info


def show_account_summary():
    profile = rh.profiles.load_account_profile()
    portfolio = rh.profiles.load_portfolio_profile()

    print("Account status:", profile.get("state", "unknown"))
    print("Buying power:   $", profile.get("buying_power", "n/a"))
    print("Portfolio value: $", portfolio.get("equity", "n/a"))

    positions = rh.account.get_open_stock_positions()
    held = [p for p in positions if float(p.get("quantity", 0)) > 0]

    print(f"\nOpen stock positions: {len(held)}")
    for p in held:
        symbol = rh.stocks.get_symbol_by_url(p["instrument"])
        qty = p["quantity"]
        print(f"  {symbol}: {qty} shares")


if __name__ == "__main__":
    connect()
    show_account_summary()
    rh.logout()
    print("\nLogged out. Session cache cleared for this run.")
