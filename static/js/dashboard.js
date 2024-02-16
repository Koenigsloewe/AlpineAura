document.addEventListener('DOMContentLoaded', function() {
        const profileInfoBtn = document.querySelector("button[title='Profile Information']");
        const profileInfoContent = document.getElementById('profileInformationContent');

        profileInfoBtn.addEventListener('click', function() {
            profileInfoContent.classList.toggle('hidden');
            // Hide other sections if necessary
        });
    });