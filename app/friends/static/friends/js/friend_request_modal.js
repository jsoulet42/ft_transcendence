function validateForm() {
	const friendRequestForm = document.getElementById('friend-request-form');
	const csrfToken = friendRequestForm.querySelector('[name=csrfmiddlewaretoken]').value;

	const formData = new FormData(friendRequestForm);

	if (!formData.get('username') && !formData.get('uuid')) {
		alert(gettext('Please enter either a username or a UUID.'));
		/* Prevent form submission */
		return false;
	}

	fetch(sendRequestUrl, {
		method: 'POST',
		headers: {
			'X-CSRFToken': csrfToken,
		},
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		var modalFooter = document.querySelector('#friend-request-modal .modal-footer');
		if (!modalFooter) {
			modalFooter = document.createElement('div');
		}

		modalFooter.classList = [];
		modalFooter.classList.add('modal-footer', 'mx-5', 'alert');

		if (data.error) {
			modalFooter.textContent = data.error;
			modalFooter.classList.add('alert-danger');
		} else {
			modalFooter.textContent = data.success;
			modalFooter.classList.add('alert-success');
		}

		const modalContent = document.querySelector('#friend-request-modal .modal-content');
		modalContent.appendChild(modalFooter);
	})
	.catch(error => {
		console.error('Error sending friend request:', error);
	});

	/* Allow form submission */
	return true;
}