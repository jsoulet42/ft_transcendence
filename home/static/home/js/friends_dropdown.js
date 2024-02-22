	document.addEventListener('DOMContentLoaded', function() {
		const friendsDropdown = document.getElementById('friends-dropdown');

		friendsDropdown.addEventListener('click', function(event) {
			const target = event.target;

			// Check if the clicked element is a button inside the dropdown
			if (target.tagName === 'BUTTON' && target.closest('.dropdown-menu')) {
				event.stopPropagation();
				event.preventDefault();
			}
		});
	});

	function createFriendsDropdown() {
		fetchFriendRequests();
		fetchFriendList();
	}

	function fetchFriendRequests() {
		fetch('/friends/requests/get/', {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrf_token,
			}
		})
		.then(response => response.json())
		.then(data => {
			const friend_requests_container = document.getElementById('friend-requests-container');
			const divider = `<li><hr class="dropdown-divider"></li>`;

			friend_requests_container.innerHTML = `<li><div class="dropdown-header">Requests</div></li>`;
			
			if (data.length === 0) {
				friend_requests_container.insertAdjacentHTML('beforeEnd', `<li>No friend requests</li>`);
			} else {
				const btn_accept = `<button type="button" class="btn btn-add" onclick="acceptFriendRequest(event)" aria-label="Accept"></button>`
				const btn_deny = `<button type="button" class="btn btn-deny" onclick="rejectFriendRequest(event)" aria-label="Reject"></button>`

				data.forEach(request => {
					const listItem = `<li class="row">`
						+ `<span class="col text-start">${request.username}</span>`
						+ `<div class="col text-end">`
						+ `${btn_accept}`
						+ `${btn_deny}`
						+ `</div>`
						+ `</li>`;
					friend_requests_container.insertAdjacentHTML('beforeEnd', listItem);
				});
			}
			
			friend_requests_container.insertAdjacentHTML('beforeEnd', divider);
		})
		.catch(error => console.error('Error fetching friend requests:', error));
	}

	function fetchFriendList() {
		fetch('/friends/list/get/', {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrf_token,
			}
		})
		.then(response => response.json())
		.then(data => {
			const friend_list_container = document.getElementById('friend-list-container');
			const divider = `<li><hr class="dropdown-divider"></li>`;

			friend_list_container.innerHTML = `<li><div class="dropdown-header">Friends</div></li>`;
			
			if (data.length === 0) {
				friend_list_container.insertAdjacentHTML('beforeEnd', `<li>You have no friends D:</li>`);
			} else {
				const btn_remove = `<button type="button" class="btn btn-deny" onclick="removeFriend(event)" aria-label="Remove"></button>`

				data.forEach(request => {
					const listItem = `<li class="row">`
						+ `<span class="col text-start">${request.username}</span>`
						+ `<div class="col text-end">`
						+ `${btn_remove}`
						+ `</div>`
						+ `</li>`;
					friend_list_container.insertAdjacentHTML('beforeEnd', listItem);
				});
			}
			
			friend_list_container.insertAdjacentHTML('beforeEnd', divider);
		})
		.catch(error => console.error('Error fetching friend list:', error));
	}

	function acceptFriendRequest(event) {
		const sender = event.target.parentNode.previousElementSibling.textContent;

		fetch(`/friends/requests/accept/${sender}/${session_user_username}/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrf_token,
			},
			body: JSON.stringify({})
		})
		.then(response => {
			if (response.ok) {
				return response.json();
			}
			throw new Error('Network response was not ok.');
		})
		.then(data => {
			createFriendsDropdown();
		})
		.catch(error => {
			console.error('Error while requesting friend accept:', error);
		});
	}

	function rejectFriendRequest(event) {
		const sender = event.target.parentNode.previousElementSibling.textContent;

		fetch(`/friends/requests/reject/${sender}/${session_user_username}/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrf_token,
			},
			body: JSON.stringify({})
		})
		.then(response => {
			if (response.ok) {
				return response.json();
			}
			throw new Error('Network response was not ok.');
		})
		.then(data => {
			createFriendsDropdown();
		})
		.catch(error => {
			console.error('Error while requesting friend reject:', error);
		});
	}

	function removeFriend(event) {
		const friend_username = event.target.parentNode.previousElementSibling.textContent;

		const formData = new FormData();
		formData.append('friend_username', friend_username);

		fetch(`/friends/remove/`, {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrf_token,
			},
			body: formData
		})
		.then(response => {
			if (response.ok) {
				return response.json();
			}
			throw new Error('Network response was not ok.');
		})
		.then(data => {
			console.log(data)
			createFriendsDropdown();
		})
		.catch(error => {
			console.error('Error while requesting friend reject:', error);
		});
	}