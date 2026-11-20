from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage, Project, Skill


class PortfolioViewTests(TestCase):
    def test_home_page_has_projects_and_hobbies_navigation(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, 'href="#projects">Projects</a>')
        self.assertContains(response, 'href="#hobbies">Hobbies</a>')
        self.assertContains(response, 'Dancing')
        self.assertContains(response, 'Music')
        self.assertContains(response, 'Outside of technology, dancing and music are two interests I enjoy.')
        self.assertContains(response, 'href="#education">Education</a>')
        self.assertContains(response, 'Computer Science')
        self.assertContains(response, 'portfolio/images/portfolio-project-preview.png')
        self.assertContains(response, 'target="_blank"')
        self.assertNotContains(response, 'portrait-orbit')
        self.assertNotContains(response, '82%')
        self.assertNotContains(response, 'proficiency')

    def test_projects_without_screenshots_keep_a_placeholder(self):
        Project.objects.create(
            title='A project without a preview',
            description='Screenshot pending.',
        )

        response = self.client.get(reverse('home'))

        self.assertContains(response, 'Screenshot not provided')

    def test_project_cards_show_only_saved_screenshot_features_and_links(self):
        project = Project.objects.create(
            title='A verified app',
            description='A project description.',
            technologies='Django, SQLite',
            key_features='Contact form\nAdmin dashboard',
            screenshot_url='https://example.com/screenshot.png',
            source_url='https://github.com/example/project',
            live_url='https://example.com',
        )

        response = self.client.get(reverse('home'))

        self.assertContains(response, project.title)
        self.assertContains(response, 'src="https://example.com/screenshot.png"')
        self.assertContains(response, 'Contact form')
        self.assertContains(response, 'https://github.com/example/project')
        self.assertContains(response, 'https://example.com')
        self.assertContains(response, 'Open full screenshot of A verified app')

    def test_home_page_renders_portfolio_and_contact_form(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Full-Stack Developer')
        self.assertContains(response, 'aria-controls="main-menu"')
        self.assertContains(response, 'data-reveal')
        self.assertContains(response, 'class="back-to-top" href="#home"')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'Namrata Jaiswal')
        self.assertNotContains(response, 'Namrta Jaiswal')
        self.assertContains(response, 'Full-stack development brings together')
        self.assertContains(response, 'The browser-facing layer')
        self.assertContains(response, 'portfolio/images/namrta-jaiswal.jpeg')
        self.assertContains(response, 'portfolio/resumes/Namrta_Jaiswal_Resume.pdf')

    def test_valid_contact_submission_is_saved_and_redirects(self):
        response = self.client.post(reverse('home'), {
            'name': 'Avery Example',
            'email': 'avery@example.com',
            'subject': 'Portfolio project',
            'message': 'I would like to discuss a project.',
        })

        self.assertRedirects(response, reverse('home'))
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(ContactMessage.objects.get().email, 'avery@example.com')

    def test_staff_dashboard_shows_contact_form_submissions(self):
        ContactMessage.objects.create(
            name='Avery Example',
            email='avery@example.com',
            subject='Portfolio project',
            message='I would like to discuss a project.',
        )
        staff = get_user_model().objects.create_user(
            username='message-manager',
            password='test-password-123',
            is_staff=True,
        )
        self.client.force_login(staff)

        response = self.client.get(reverse('dashboard'))

        self.assertContains(response, 'Recent messages')
        self.assertContains(response, 'Portfolio overview')
        self.assertNotContains(response, 'welcome-art')
        self.assertNotContains(response, 'floating-tag')
        self.assertContains(response, 'Portfolio project')
        self.assertContains(response, 'avery@example.com')
        self.assertContains(response, 'I would like to discuss a project.')

    def test_invalid_contact_submission_is_not_saved(self):
        response = self.client.post(reverse('home'), {
            'name': 'Avery Example',
            'email': 'not-an-email',
            'subject': 'Portfolio project',
            'message': 'I would like to discuss a project.',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(ContactMessage.objects.count(), 0)


class PortfolioDashboardTests(TestCase):
    def setUp(self):
        self.staff = get_user_model().objects.create_user(
            username='portfolio-manager',
            password='test-password-123',
            is_staff=True,
        )

    def test_dashboard_requires_staff_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('dashboard')}",
            fetch_redirect_response=False,
        )

        visitor = get_user_model().objects.create_user(
            username='visitor',
            password='test-password-123',
        )
        self.client.force_login(visitor)
        self.assertEqual(self.client.get(reverse('dashboard')).status_code, 403)

    def test_staff_can_create_edit_and_delete_skill_and_project(self):
        self.client.force_login(self.staff)

        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'Profile & resume')
        self.assertContains(response, 'Add project')

        invalid_skill = self.client.post(reverse('skill_create'), {})
        self.assertEqual(invalid_skill.status_code, 200)
        self.assertTrue(invalid_skill.context['form'].errors)

        response = self.client.post(reverse('skill_create'), {
            'name': 'Accessibility',
            'category': 'Front-end',
            'proficiency': 80,
            'display_order': 1,
        })
        self.assertRedirects(response, reverse('dashboard'))
        skill = Skill.objects.get(name='Accessibility')
        self.assertEqual(self.client.get(reverse('skill_edit', args=[skill.pk])).status_code, 200)
        response = self.client.post(reverse('skill_edit', args=[skill.pk]), {
            'name': 'Web accessibility',
            'category': 'Front-end',
            'proficiency': 90,
            'display_order': 1,
        })
        self.assertRedirects(response, reverse('dashboard'))
        skill.refresh_from_db()
        self.assertEqual(skill.name, 'Web accessibility')
        self.assertEqual(skill.proficiency, 90)
        self.client.post(reverse('skill_delete', args=[skill.pk]))
        self.assertFalse(Skill.objects.filter(pk=skill.pk).exists())

        invalid_project = self.client.post(reverse('project_create'), {})
        self.assertEqual(invalid_project.status_code, 200)
        self.assertTrue(invalid_project.context['form'].errors)

        response = self.client.post(reverse('project_create'), {
            'title': 'A sample project',
            'description': 'A project used to test portfolio management.',
            'technologies': 'Django, Python',
            'key_features': 'Contact form\nResponsive layout',
            'screenshot_url': 'https://example.com/screenshot.png',
            'screenshot_path': 'portfolio/images/portfolio-project-preview.png',
            'theme': 'moss',
            'display_order': 2,
        })
        self.assertRedirects(response, reverse('dashboard'))
        project = Project.objects.get(title='A sample project')
        self.assertEqual(project.key_features, 'Contact form\nResponsive layout')
        self.assertEqual(project.screenshot_url, 'https://example.com/screenshot.png')
        self.assertEqual(project.screenshot_path, 'portfolio/images/portfolio-project-preview.png')
        self.assertEqual(self.client.get(reverse('project_edit', args=[project.pk])).status_code, 200)
        response = self.client.post(reverse('project_edit', args=[project.pk]), {
            'title': 'Updated project',
            'description': 'Updated project details.',
            'technologies': 'Django',
            'theme': 'sand',
            'display_order': 1,
        })
        self.assertRedirects(response, reverse('dashboard'))
        project.refresh_from_db()
        self.assertEqual(project.title, 'Updated project')
        self.assertEqual(project.theme, 'sand')
        self.client.post(reverse('project_delete', args=[project.pk]))
        self.assertFalse(Project.objects.filter(pk=project.pk).exists())

    def test_resume_renders_printable_profile_and_skills(self):
        response = self.client.get(reverse('resume'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Namrata Jaiswal')
        self.assertContains(response, 'HTML &amp; CSS')
        self.assertContains(response, 'Download CV')
        self.assertContains(response, 'portfolio/resumes/Namrta_Jaiswal_Resume.pdf')

    def test_staff_can_update_resume_profile(self):
        self.client.force_login(self.staff)
        response = self.client.post(reverse('dashboard'), {
            'full_name': 'Namrata Jaiswal',
            'job_title': 'Python Developer',
            'email': 'namrta@example.com',
            'phone': '1234567890',
            'location': 'Jaipur',
            'summary': 'Python and Django developer.',
            'education': 'Bachelors degree',
            'experience': 'Junior Developer, Example Co.',
            'linkedin_url': 'https://www.linkedin.com/in/namrta',
            'github_url': 'https://github.com/namrta',
        })

        self.assertRedirects(response, reverse('dashboard'))
        resume_response = self.client.get(reverse('resume'))
        self.assertContains(resume_response, 'Python Developer')
        self.assertContains(resume_response, 'namrta@example.com')
        self.assertContains(resume_response, 'Bachelors degree')
