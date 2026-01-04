"""Communication templates (public, generic)."""

from __future__ import annotations

from typing import Dict

TEMPLATES: Dict[str, str] = {
    "technical_inquiry": (
        "Subject: [Project] {project_name} - {process} Technical Inquiry\n\n"
        "Dear FAE team,\n\n"
        "We have a question regarding:\n"
        "- Issue: {issue_description}\n"
        "- Urgency: {urgency}\n\n"
        "Could you please provide guidance or relevant application notes?\n"
        "If needed, we can share simplified schematics/logs.\n\n"
        "Thanks,\n"
        "{sender}"
    ),
    "drc_waiver_request": (
        "Subject: [Waiver] {project_name} - {process} DRC Waiver Request\n\n"
        "Dear FAE team,\n\n"
        "We request a waiver for the following DRC rule:\n"
        "- Rule ID / Layer: {rule_id}\n"
        "- Location / Instance: {location}\n"
        "- Rationale: {issue_description}\n"
        "- Impact: Functionally benign, no reliability risk (please confirm)\n\n"
        "Attached: screenshots, layout clip, signoff report excerpt.\n"
        "Please advise acceptance criteria and any required mitigations.\n\n"
        "Regards,\n"
        "{sender}"
    ),
    "tapeout_schedule": (
        "Subject: {project_name} Tape-out Schedule Alignment ({process})\n\n"
        "Dear FAE team,\n\n"
        "We plan the following milestones:\n"
        "- Final netlist freeze: {netlist_freeze}\n"
        "- Signoff complete: {signoff_complete}\n"
        "- GDS release target: {gds_release}\n\n"
        "Please confirm mask shop lead time and any holiday/maintenance windows.\n\n"
        "Thanks,\n"
        "{sender}"
    ),
    "yield_issue_report": (
        "Subject: Yield Issue Report - {project_name} ({process})\n\n"
        "Dear FAE team,\n\n"
        "Summary of issue:\n"
        "- Symptom: {issue_description}\n"
        "- Lots / wafers affected: {lots}\n"
        "- Test conditions: {test_conditions}\n"
        "- Urgency: {urgency}\n\n"
        "Attachments: wafer maps, fail logs, pareto.\n"
        "Please advise next debug steps and recommended monitors.\n\n"
        "Regards,\n"
        "{sender}"
    ),
    "respin_request": (
        "Subject: Respin Request - {project_name} ({process})\n\n"
        "Dear FAE team,\n\n"
        "We need a respin due to:\n"
        "- Issue: {issue_description}\n"
        "- Impact: {impact}\n"
        "- Urgency: {urgency}\n\n"
        "Kindly share updated mask schedule and any NPI requirements.\n\n"
        "Thanks,\n"
        "{sender}"
    ),
}



