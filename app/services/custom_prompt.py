from app.schemas.query import TelemetrySearchMatch


def build_diagnostic_prompt(query: str, matches: list[TelemetrySearchMatch]) -> str:
    context_parts: list[str] = []
    for match in matches:
        part: str = f"Log entry: {match.document}"
        if match.metadata:
            meta_str = ", ".join(f"{k}: {v}" for k, v in match.metadata.items())

            part += f" | Metrics: {meta_str}"
        context_parts.append(part)

    context = "\n---\n".join(context_parts)
    return f"""
        You are an industrial telemetry analyst. Given the following historical log entries, diagnose the probable root cause of the described issue.

        Issue: {query}

        Relevant Historical Logs:
        {context}

        If the issue contains a direct question about specific metrics, answer that question explicitly with a clear yes/no and cite the evidence. 

        Reiterating, for direct questions answer specifically yes or no, whether the log contains issues or not. If the question about the metric is about a potential issue that does not exist in the logs, answer the question explicitly then review the logs and indicate probable diagnostic issues that should be investigated. Avoid overfitting queries.

        Then provide the root-cause analysis (if any) and recommended next steps.
    """