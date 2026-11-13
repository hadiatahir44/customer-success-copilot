"""
demo_results.py
Saved example analyses for the three sample accounts.
They let anyone try the app instantly, with no API key and no cost.
All companies and people are fictional.
"""

DEMO_RESULTS = {
    "At-risk account (Northwind Logistics)": {
        "account_name": "Northwind Logistics",
        "summary": "Priya is still positive about the product, but three weeks of slow dashboards and the loss of their main admin have pulled usage down. Leadership is weighing alternatives ahead of a Q1 renewal, so this account needs attention now.",
        "health_score": 42,
        "health_label": "At Risk",
        "churn_risk": {
            "level": "High",
            "reasons": [
                {"reason": "Leadership is evaluating competitors before renewal",
                 "evidence": "leadership is \"looking at other options\" before renewal"},
                {"reason": "Usage dropped after the main admin left",
                 "evidence": "Usage dropped after their main admin, Tom, left the company last month"},
                {"reason": "Ongoing performance problem is frustrating the team",
                 "evidence": "frustrated with the reporting dashboard loading slowly for about 3 weeks"},
            ],
        },
        "stakeholders": [
            {"name": "Priya", "role": "Ops Manager", "stance": "Champion",
             "note": "Still positive about the product and wants it to work"},
            {"name": "Tom", "role": "Former admin", "stance": "Unknown",
             "note": "Left the company last month and has not been replaced"},
            {"name": "Leadership", "role": "Unknown", "stance": "Decision Maker",
             "note": "Looking at other options before renewal"},
        ],
        "single_threaded": True,
        "commitments": [
            {"what": "Send a fix timeline from engineering", "owner": "Us", "due": "Friday"},
            {"what": "Training session for the two new team members", "owner": "Us", "due": "Not stated"},
        ],
        "next_actions": [
            {"action": "Get a firm ETA on the dashboard fix from engineering before Friday", "priority": "High"},
            {"action": "Ask Priya for an intro to the leader reviewing alternatives", "priority": "High"},
            {"action": "Schedule a training session for the two new team members", "priority": "Medium"},
            {"action": "Confirm the exact renewal date", "priority": "Medium"},
        ],
        "expansion_signals": [],
        "missing_info": [
            "Exact renewal date",
            "Who is replacing Tom as the admin",
            "Which leader is evaluating alternatives",
            "Current usage numbers",
        ],
        "follow_up_email": {
            "subject": "Dashboard fix timeline and training for your team",
            "body": "Hi Priya,\n\nThank you for being so open on our call. I know the slow dashboard has been frustrating for the team these past few weeks, and I want to make sure we fix it properly.\n\nI am working with our engineering team now and will send you a clear timeline by Friday.\n\nI would also love to set up a training session for your two new team members. Could you share a few times that work for them next week?\n\nIf it would help, I am happy to join a short call with your leadership team to walk through the plan.\n\nBest,\n[Your name]",
        },
        "internal_escalation": {
            "needed": True,
            "team": "Engineering",
            "urgency": "High",
            "message": "Northwind Logistics has had slow reporting dashboard load times for about 3 weeks. Leadership is evaluating competitors ahead of a Q1 renewal, and usage has already dropped. I promised the customer a fix timeline by Friday. Can we get an owner and an ETA today?",
        },
    },

    "Healthy account with upsell (Brightpath Health)": {
        "account_name": "Brightpath Health",
        "summary": "Brightpath's rollout went better than expected, with daily use of automation features and faster support response times. A new regional office in March could mean 40 more seats, and the team is exploring an API integration.",
        "health_score": 88,
        "health_label": "Healthy",
        "churn_risk": {
            "level": "Low",
            "reasons": [
                {"reason": "Strong satisfaction with the rollout",
                 "evidence": "the rollout went \"better than expected\""},
                {"reason": "High daily engagement with key features",
                 "evidence": "Sara's team uses the automation features daily"},
            ],
        },
        "stakeholders": [
            {"name": "Daniel", "role": "VP Customer Experience", "stance": "Decision Maker",
             "note": "Happy with results and controls the expansion budget"},
            {"name": "Sara", "role": "Team Lead", "stance": "Champion",
             "note": "Daily power user exploring the API"},
        ],
        "single_threaded": False,
        "commitments": [
            {"what": "Send API documentation", "owner": "Us", "due": "This week"},
            {"what": "Set up a call with our solutions engineer", "owner": "Us", "due": "Not stated"},
            {"what": "Share the expansion budget timeline", "owner": "Daniel", "due": "After next week's planning meeting"},
        ],
        "next_actions": [
            {"action": "Send the API documentation to Sara this week", "priority": "High"},
            {"action": "Book the solutions engineer call for the CRM integration", "priority": "High"},
            {"action": "Prepare a 40-seat expansion proposal for the March office", "priority": "Medium"},
            {"action": "Ask Daniel for a short case study or reference", "priority": "Low"},
        ],
        "expansion_signals": [
            "New regional office opening in March may need 40 more seats",
            "Interest in the API for connecting their internal CRM",
        ],
        "missing_info": [
            "Contract renewal date",
            "Expansion budget amount and timing",
            "Who signs off on new seats",
        ],
        "follow_up_email": {
            "subject": "Great check-in, plus API docs and next steps",
            "body": "Hi Daniel and Sara,\n\nThank you for the great check-in. It is wonderful to hear the rollout went better than expected and that the team's response times have improved.\n\nSara, I will send over the API documentation this week and set up a call with our solutions engineer to talk through connecting your CRM.\n\nDaniel, congratulations on the new regional office. Whenever you are ready after your planning meeting, I would be glad to put together a plan for the additional seats.\n\nBest,\n[Your name]",
        },
        "internal_escalation": {"needed": False, "team": "None", "urgency": "Low", "message": ""},
    },

    "Critical escalation (Cedar Finance)": {
        "account_name": "Cedar Finance",
        "summary": "A failed data export since last Tuesday's update is blocking Cedar Finance's month-end close, and their support ticket has gone five days without a clear update. With one remaining contact and renewal in six weeks, this account is at serious risk.",
        "health_score": 18,
        "health_label": "Critical",
        "churn_risk": {
            "level": "High",
            "reasons": [
                {"reason": "Product issue is blocking a critical business process",
                 "evidence": "This is blocking our month-end close."},
                {"reason": "Customer is threatening internal escalation",
                 "evidence": "If this isn't fixed by Monday we will need to escalate internally."},
                {"reason": "Slow support response is eroding trust",
                 "evidence": "Support ticket has been open 5 days with no clear update."},
                {"reason": "Relationship depends on one contact",
                 "evidence": "Marcus is our only contact there. Previous champion left in the summer."},
            ],
        },
        "stakeholders": [
            {"name": "Marcus", "role": "IT Director", "stance": "Detractor",
             "note": "Frustrated and threatening escalation over the blocked export"},
        ],
        "single_threaded": True,
        "commitments": [
            {"what": "Fix the failing data export", "owner": "Us", "due": "Monday (customer deadline)"},
        ],
        "next_actions": [
            {"action": "Escalate to engineering today and get a named owner for the export bug", "priority": "High"},
            {"action": "Call Marcus today to acknowledge the issue and share a plan", "priority": "High"},
            {"action": "Offer a workaround for the month-end close if possible", "priority": "High"},
            {"action": "Identify a second contact or new champion before renewal", "priority": "Medium"},
        ],
        "expansion_signals": [],
        "missing_info": [
            "Root cause of the export failure",
            "Whether a workaround exists",
            "Who signs the renewal",
        ],
        "follow_up_email": {
            "subject": "Your data export issue: our plan and next steps",
            "body": "Hi Marcus,\n\nI am sorry about the data export failures and the lack of updates on your ticket. I understand this is blocking your month-end close, and that is not acceptable.\n\nI have escalated this to our engineering team today, and I am personally following it until it is resolved. I will send you an update by end of day today with the cause and a timeline, and I will also check if we can offer a workaround so your close is not held up.\n\nCould we have a quick call today or tomorrow?\n\nBest,\n[Your name]",
        },
        "internal_escalation": {
            "needed": True,
            "team": "Engineering",
            "urgency": "High",
            "message": "Cedar Finance's data export has failed for all users since last Tuesday's update and is blocking their month-end close. Their ticket has been open 5 days with no clear update. The customer's deadline is Monday, renewal is in 6 weeks and we have only one contact left. Need an owner, root cause and ETA today, plus a possible workaround.",
        },
    },
}
