Tabulation resource: - users - judges - events - participants

users: ------------------------ checked: done

GET: /api/users
Fetch all users

GET: /api/users/{id}
Fetch specific user

POST: /api/users
Create a new user
Expected data format to submit:
{
"username": str,
"email": str,
"password": str,
"firstname": str,
"middlename": str,
"lastname": str,
"role_id": int,
"organization_id": int
}

PUT: /api/users/{user_id}
Update user information
Expected data format to submit:
{
"username": str,
"email": str,
"password": str,
"firstname": str,
"middlename": str,
"lastname": str,
"is_active": int,
"role_id": int,
"organization_id": int
}

DELETE: /api/users/{user_id}
Delete user

judges: ------------------------ checked: done

GET: /api/judges
Fetch all judges

GET: /api/judges/{judge_id}
Fetch specific judge

POST: /api/judges
Assign user into new judge
Expected data format to submit:
{
"user_id": int
}

DELETE: /api/judges/{judge_id}
Delete judge

events: ------------------------ checked: done

GET: /api/events
Fetch all events

GET: /api/events/{event_id}
Fetch specific event

GET: /api/events/{event_id}/all_criterias
Fetch all criterias from a specific event

GET: /api/events/{event_id}/find_criteria/{criteria_id}
Fetch a specific criteria from a specific event

POST: /api/events
Create a new event
Expected data format to submit:
{
"name": str,
"description": str,
"img_path": str,
"event_type_id": int,
"organization_id": int
}

POST: /api/events/{event_id}/add_judge
Add judge to a specific event
Expected data format to submit:
{
"judge_id": int
}

POST: /api/events/{event_id}/add_participant
Add participant to a specific event
{
"participant_id": int
}

PUT: /api/events/{event_id}
Update specific event
Expected data format to submit:
{
"name": str,
"description": str,
"img_path": str,
"is_active": int,
"event_type_id": int,
"organization_id": int
}

DELETE: /api/events/{event_id}
Delete specific event

DELETE: /api/events/{event_id}/delete_judge/{judge_id}
Delete specific judge from a specific event

DELETE: /api/events/{event_id}/delete_participant/{participant_id}
Delete specific participant from a specific event

participants: ------------------------ checked: done

GET: /api/participants
Fetch all participants

GET: /api/participants/{participant_id}
Fetch specific participant

POST: /api/participants
Create a new participant
Expected data format to submit:
{
"email": str,
"firstname": str,
"middlename": str,
"lastname": str,
"img_path": str,
"participant_type_id": int,
"participant_team_id": int,
"organization_id": int
}

PUT: /api/participants/{participant_id}
Update specific participant
{
"email": str,
"firstname": str,
"middlename": str,
"lastname": str,
"img_path": str,
"is_active": int,
"participant_type_id": int,
"participant_team_id": int
}

DELETE: /api/participants/{participant_id}
Delete specific participant

roles: ------------------------ checked: done

GET: /api/roles
Fetch all roles

GET: /api/roles/{role_id}
Fetch specific role

POST: /api/roles
Create a new role
Expected data format to submit:
{
"name": str,
"code": int
}

PUT: /api/roles/{role_id}
Update specific role
Expected data format to submit:
{
"name": str,
"code": int
}

DELETE: /api/roles/{role_id}
Delete specific role

organization: ------------------------ checked: done

GET: /api/organizations
Fetch all organizations

GET: /api/organizations/{organization_id}
Fetch specific organization

POST: /api/organizations
Create a new organization
Expected data format to submit:
{
"name": str,
"description": str,
"organization_type_id": int
}

PUT: /api/organizations/{organization_id}
Update specific organization
{
"name": str,
"description": str,
"organization_type_id": int
}

DELETE: /api/organizations/{organization_id}
Delete specific organization

organization-types: ------------------------ checked: done

GET: /api/organization-types
Fetch all organization types

GET: /api/organization-types/{organization_type_id}
Fetch specific organization type

POST: /api/organization-types
Create a new organization type
Expected data format to submit:
{
"name": str,
"description": str
}

PUT: /api/organization-types/{organization_type_id}
Update specific organization type
Expected data format to submit:
{
"name": str,
"description": str
}

DELETE: /api/organization-types/{organization_type_id}
Delete specific organization type

event-types: ------------------------ checked: done

GET: /api/event-types
Fetch all event types

GET: /api/event-types/{event_type_id}
Fetch specific event type

POST: /api/event-types
Create a new event type
Expected data format to submit:
{
"name": str
}

PUT: /api/event-types/{event_type_id}
Update specific event type
Expected data format to submit:
{
"name": str
}

DELETE: /api/event-types/{event_type_id}
Delete specific event type

participant-teams: ------------------------ checked: done

GET: /api/participant-teams
Fetch all participant teams

GET: /api/participant-teams/{participant_team_id}
Fetch specific participant team

POST: /api/participant-teams
Create a new participant team
Expected data format to submit:
{
"name": str,
"description": str
}

PUT: /api/participant-teams/{participant_team_id}
Update specific participant team
Expected data format to submit:
{
"name": str,
"description": str
}

DELETE: /api/participant-teams/{participant_team_id}
Delete specific participant team

participant-types: ------------------------ checked: done

GET: /api/participant-types
Fetch all participant types

GET: /api/participant-types/{participant_type_id}
Fetch specific participant type

POST: /api/participant-types
Create a new participant type
Expected data format to submit:
{
"name": str,
"description": str
}

PUT: /api/participant-types/{participant_type_id}
Update specific participant type
Expected data format to submit:
{
"name": str,
"description": str
}

DELETE: /api/participant-types/{participant_type_id}
Delete specific participant type

event-scores: ------------------------

GET: /api/event-scores
Fetch all event scores

GET: /api/event-scores/{event_score_id}
Fetch specific event score

POST: /api/event-scores
Create a new event score
Expected data format to submit:
"score": float,
"event_judge_id": int,
"event_participant_id": int,
"criteria_id": int
}

PUT: /api/event-scores/{event_score_id}
Update specific event score
Expected data format to submit:
{
"score": float,
"event_judge_id": int,
"event_participant_id": int,
"criteria_id": int
}

DELETE: /api/event-scores/{event_score_id}
Delete specific event score
