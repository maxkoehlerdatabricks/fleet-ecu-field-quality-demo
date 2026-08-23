#!/usr/bin/env python3
"""Run one SQL statement against a warehouse via the Databricks SDK.
Works across CLI versions (the CLI has no `sql query` subcommand).

Usage:
  python3 deploy/run_sql.py <profile> <warehouse_id> "<SQL>"
"""
import sys
from databricks.sdk import WorkspaceClient

profile, warehouse_id, sql = sys.argv[1], sys.argv[2], sys.argv[3]
w = WorkspaceClient(profile=profile)
r = w.statement_execution.execute_statement(
    warehouse_id=warehouse_id, statement=sql, wait_timeout="50s")
state = r.status.state.value
print(f"[{state}] {sql[:80]}")
if state == "FAILED":
    print("ERROR:", r.status.error.message if r.status.error else "unknown")
    sys.exit(1)
