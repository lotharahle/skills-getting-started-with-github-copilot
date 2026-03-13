from src import app as app_module


def test_get_activities_returns_dictionary(client):
    response = client.get('/activities')

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert 'Chess Club' in payload


def test_signup_success_adds_participant(client):
    activity_name = 'Chess Club'
    email = 'new.student@mergington.edu'

    response = client.post(f'/activities/{activity_name}/signup', params={'email': email})

    assert response.status_code == 200
    assert response.json() == {'message': f'Signed up {email} for {activity_name}'}
    assert email in app_module.activities[activity_name]['participants']


def test_signup_duplicate_returns_400(client):
    activity_name = 'Chess Club'
    email = app_module.activities[activity_name]['participants'][0]

    response = client.post(f'/activities/{activity_name}/signup', params={'email': email})

    assert response.status_code == 400
    assert response.json()['detail'] == 'Student already signed up for this activity'


def test_signup_full_activity_returns_400(client):
    activity_name = 'Chess Club'
    activity = app_module.activities[activity_name]
    activity['participants'] = [f'student{i}@mergington.edu' for i in range(activity['max_participants'])]

    response = client.post(
        f'/activities/{activity_name}/signup',
        params={'email': 'overflow@mergington.edu'},
    )

    assert response.status_code == 400
    assert response.json()['detail'] == 'Activity is full'


def test_signup_unknown_activity_returns_404(client):
    response = client.post('/activities/Unknown Club/signup', params={'email': 'x@mergington.edu'})

    assert response.status_code == 404
    assert response.json()['detail'] == 'Activity not found'


def test_unregister_success_removes_participant(client):
    activity_name = 'Gym Class'
    email = app_module.activities[activity_name]['participants'][0]

    response = client.delete(f'/activities/{activity_name}/signup', params={'email': email})

    assert response.status_code == 200
    assert response.json() == {'message': f'Unregistered {email} from {activity_name}'}
    assert email not in app_module.activities[activity_name]['participants']


def test_unregister_missing_participant_returns_404(client):
    response = client.delete(
        '/activities/Gym Class/signup',
        params={'email': 'missing.student@mergington.edu'},
    )

    assert response.status_code == 404
    assert response.json()['detail'] == 'Student is not signed up for this activity'


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete('/activities/Unknown Club/signup', params={'email': 'x@mergington.edu'})

    assert response.status_code == 404
    assert response.json()['detail'] == 'Activity not found'
