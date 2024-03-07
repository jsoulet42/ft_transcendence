function initializePage() {
	const friendsDropdowns = document.querySelectorAll('.friends-dropdown');
	if (!friendsDropdowns) {
		return;
	}

	friendsDropdowns.forEach(initializeFriendsDropdown);
}

document.addEventListener('DOMContentLoaded', initializePage);
document.addEventListener('htmx:afterOnLoad', initializePage);

function initializeFriendsDropdown(friendsDropdown) {
	friendsDropdown.addEventListener('click', function(event) {
		const target = event.target;

		// Check if the clicked element is a button inside the dropdown
		if (target.tagName === 'BUTTON' && target.closest('.friends-dropdown-menu')) {
			event.stopPropagation();
			event.preventDefault();
		}
	});
	
	const friendsDropDownToggle = friendsDropdown.querySelector('.friends-dropdown-toggle');
	if (!friendsDropDownToggle) {
		return;
	}

	friendsDropDownToggle.addEventListener('click', function() {
		fetchFriendsDropdown(friendsDropdown);
	});

	const friendsDropdownRefreshButton = friendsDropdown.querySelector('.friends-dropdown-refresh');
	if (!friendsDropdownRefreshButton) {
		return;
	}
	friendsDropdownRefreshButton.addEventListener('click', function() {
		fetchFriendsDropdown(friendsDropdown);
	});
}

function fetchFriendsDropdown(friendsDropdown) {
	fetchFriendRequests(friendsDropdown);
	fetchFriendList(friendsDropdown);
}

function fetchFriendRequests(friendsDropdown) {
	fetch(friendsDropdown.dataset.getRequestsUrl, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': friendsDropdown.dataset.csrfToken,
		}
	})
	.then(response => response.json())
	.then(data => {
		const friendRequestsContainer = friendsDropdown.querySelector('.friend-requests-container');
		const divider = document.createElement('li');

		friendRequestsContainer.innerHTML = `<li><div class="dropdown-header">` + gettext('Requests') + `</div></li>`;
		divider.innerHTML = '<hr class="dropdown-divider">';

		if (data.length === 0) {
			friendRequestsContainer.insertAdjacentHTML('beforeEnd', `<li>` + gettext('No friend requests') + `</li>`);
		} else {
			const listItemTemplate = document.createElement('li');
			const btnContainer = document.createElement('div');
			const btn_accept = document.createElement('button');
			const btn_decline = document.createElement('button');

			listItemTemplate.classList.add('row');
			btnContainer.classList.add('col', 'text-end');

			btn_accept.type = 'button';
			btn_accept.classList.add('btn', 'btn-add');
			btn_accept.setAttribute('aria-label', gettext('Accept'));
			btn_accept.setAttribute('title', gettext('Accept'));
			
			btn_decline.type = 'button';
			btn_decline.classList.add('btn', 'btn-deny');
			btn_decline.setAttribute('aria-label', gettext('Decline'));
			btn_accept.setAttribute('title', gettext('Decline'));

			btnContainer.appendChild(btn_accept);
			btnContainer.appendChild(btn_decline);
			listItemTemplate.appendChild(btnContainer);

			data.forEach(request => {
				const listItem = listItemTemplate.cloneNode(true);
				
				listItem.innerHTML = `<span class="col text-start">${request.username}</span>`
					+ listItem.innerHTML;

				listItem.querySelector('.btn-add').addEventListener('click',
					(event) => acceptFriendRequest(event, friendsDropdown));
				listItem.querySelector('.btn-deny').addEventListener('click',
					(event) => declineFriendRequest(event, friendsDropdown));

				friendRequestsContainer.appendChild(listItem);
			});
		}
		friendRequestsContainer.appendChild(divider);
	})
	.catch(error => console.error(gettext('Error fetching friend requests: '), error));
}

function fetchFriendList(friendsDropdown) {
	fetch(friendsDropdown.dataset.getFriendListUrl, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': friendsDropdown.dataset.csrfToken,
		}
	})
	.then(response => response.json())
	.then(data => {
		const friendListContainer = friendsDropdown.querySelector('.friend-list-container');
		const divider = document.createElement('li');

		friendListContainer.innerHTML = `<li><div class="dropdown-header">` + gettext('Friends') + `</div></li>`;
		divider.innerHTML = '<hr class="dropdown-divider">';

		if (data.length === 0) {
			friendListContainer.appendChild(document.createElement('li')).textContent = gettext('You have no friends D:');
		} else {
			const statusClasses = {
				'Online': 'online',
				'Ingame': 'ingame',
				'Offline': 'offline'
			};

			const statusOrder = ['Online', 'Ingame', 'Offline'];
			const listItemTemplate = document.createElement('li');
			const btnContainer = document.createElement('div');
			const btnRemove = document.createElement('button');

			listItemTemplate.classList.add('row');

			btnContainer.classList.add('col', 'text-end');

			btnRemove.type = 'button';
			btnRemove.classList.add('btn', 'btn-deny');
			btnRemove.setAttribute('aria-label', gettext('Remove'));
			btnRemove.setAttribute('title', gettext('Remove'));

			btnContainer.appendChild(btnRemove);
			listItemTemplate.appendChild(btnContainer);

			data.sort((a, b) => statusOrder.indexOf(a.status) - statusOrder.indexOf(b.status));

			data.forEach(request => {
				const listItem = listItemTemplate.cloneNode(true);

				listItem.classList.add(statusClasses[request.status]);
				listItem.innerHTML = `<span class="col text-start">${request.username}</span>`
					+ listItem.innerHTML;

				listItem.querySelector('.btn-deny').addEventListener('click',
					(event) => removeFriend(event, friendsDropdown));

				friendListContainer.appendChild(listItem);
			});
		}
		friendListContainer.appendChild(divider);
	})
	.catch(error => console.error(gettext('Error fetching friend list: '), error));
}

function acceptFriendRequest(event, friendsDropdown) {
	const sender = event.target.parentNode.previousElementSibling.textContent;
	const formData = new FormData();

	formData.append('sender_username', sender);
	formData.append('receiver_username', friendsDropdown.dataset.sessionUserUsername);

	fetch(friendsDropdown.dataset.acceptRequestUrl, {
		method: 'POST',
		headers: {
			'X-CSRFToken': friendsDropdown.dataset.csrfToken,
		},
		body: formData
	})
	.then(response => {
		if (response.ok) {
			return response.json();
		}
		throw new Error(gettext('Network response was not ok.'));
	})
	.then(data => {
		fetchFriendsDropdown(friendsDropdown);
	})
	.catch(error => {
		console.error(gettext('Error while requesting friend accept: '), error);
	});
}

function declineFriendRequest(event, friendsDropdown) {
	const sender = event.target.parentNode.previousElementSibling.textContent;
	const formData = new FormData();
	
	formData.append('sender_username', sender);
	formData.append('receiver_username', friendsDropdown.dataset.sessionUserUsername);

	fetch(friendsDropdown.dataset.declineRequestUrl, {
		method: 'POST',
		headers: {
			'X-CSRFToken': friendsDropdown.dataset.csrfToken,
		},
		body: formData
	})
	.then(response => {
		if (response.ok) {
			return response.json();
		}
		throw new Error(gettext('Network response was not ok.'));
	})
	.then(data => {
		fetchFriendsDropdown(friendsDropdown);
	})
	.catch(error => {
		console.error(gettext('Error while requesting friend reject: '), error);
	});
}

function removeFriend(event, friendsDropdown) {
	const friend_username = event.target.parentNode.previousElementSibling.textContent;
	const formData = new FormData();
	
	formData.append('friend_username', friend_username);

	fetch(friendsDropdown.dataset.removeFriendUrl, {
		method: 'POST',
		headers: {
			'X-CSRFToken': friendsDropdown.dataset.csrfToken,
		},
		body: formData
	})
	.then(response => {
		if (response.ok) {
			return response.json();
		}
		throw new Error(gettext('Network response was not ok.'));
	})
	.then(data => {
		fetchFriendsDropdown(friendsDropdown);
	})
	.catch(error => {
		console.error(gettext('Error while requesting friend reject: '), error);
	});
}