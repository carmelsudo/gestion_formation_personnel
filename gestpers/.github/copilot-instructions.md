# Gestpers - AI Agent Instructions

## Project Overview

**Gestpers** is a Django 5.2 application for managing training/formation submissions (demandes de formations) across organizational services and users. It's a personnel/HR management system focused on training request workflow and service hierarchy management.

## Architecture & Components

### Core Structure (3 Django Apps)

1. **Formation** - Training/formation management

   - Models: `Formation`, `FormationStatus`
   - Routes: `/formation/` (list formations), `/formation/demandes/` (list requests)
   - Templates: `formations.html`, `soumissions.html`

2. **Service** - Organizational hierarchy management

   - Models: `Service` (hierarchical with parent/child), `ServiceGerant` (employee-service assignments)
   - Service types: SERVICE, DIVISION, LABO_PEDAGOGIQUE, LABO_RECHERCHE, ATELIER
   - Routes: `/service/` (currently empty)

3. **Userprofile** - User management (root URL)
   - Model: `User` (extends Django AbstractUser with avatar, groupe fields)
   - Routes: `/` (home)
   - Views: Basic home page template

### Data Flow Patterns

- **Formation**: Can target either a Service (cible='service') OR a User (cible='user'), never both
- **Service**: Self-referential (parent relationships) to support hierarchies
- **Status Tracking**: Dual status system - Formation has statut field, FormationStatus tracks user-level approval (valide/refuse)

## Key Conventions & Patterns

### URL Routing

- Root app URLs in [gestpers/urls.py](gestpers/urls.py)
- App-specific paths prefixed: `/formation/`, `/service/`, root `/` for Userprofile
- Formation has two views: empty string (formations) and `demandes` (requests)

### Template Structure

- Base template: [template/index.html](template/index.html) (not shown - contains CSS variables, extends blocks)
- Subpages extend index.html with `{% block maincontent %}` and `{% block script %}`
- **Important**: Frontend is MOCK-HEAVY - templates use hardcoded JavaScript data arrays (e.g., `formationsData`, `myFormationsData`)
- No actual Django context variables passed to templates yet; all data is hardcoded in template JS

### Frontend Conventions ([soumissions.html](template/soumissions.html) example)

- Tabbed interface using toggle pattern: `.toggle-btn.active` class switches content
- Pagination: items per page via `itemsPerPage` variable (define in template)
- Filtering: Statut, Service dropdowns with "all" option
- Sorting: Click column header (data-sort attribute) to sort ascending/descending
- Search: Client-side filter on titre, auteur, objectifs
- Status badges: CSS classes like `statut-en_attente`, `statut-valide` with color coding

### Model Field Patterns

- TextChoices for enums (not ChoiceField - check Formation, Service models for syntax)
- ForeignKey relationships default to `on_delete=models.SET_NULL, null=True, blank=True`
- User relationships use: `from ..Userprofile.models import User`
- Image fields use: `upload_to='formations/'` or `upload_to='images'`

## Common Tasks & Workflows

### Adding a New Frontend Feature

1. Add mock data array to template script section
2. Create render function (e.g., `renderAvailableFormations()`)
3. Add toggle/tab logic if needed
4. Wire pagination, search, filtering separately
5. Add action button handlers (edit, delete, view)

**Example**: In [soumissions.html#L432-L444](template/soumissions.html#L432-L444), formations data arrays define structure for both tables.

### Adding Backend API Endpoint

1. Create view function in app/views.py
2. Add path to app/urls.py (with from .views import \*)
3. Include in root gestpers/urls.py
4. Replace template mock data with fetch() calls
5. Ensure response JSON matches template field names (titre, auteur, cible_service, statut, etc.)

### Database Modifications

- Run migrations: `python manage.py makemigrations && python manage.py migrate`
- Custom User model already in use - extend [Userprofile/models.py](Userprofile/models.py), not Django auth

## Critical Issues & TODOs

### Current Limitations

- No apps registered in INSTALLED_APPS (Formation, Service, Userprofile missing) - will break migrations/admin
- Service and Userprofile views are minimal/empty
- TextChoices syntax may be invalid - should use `choices=[]` tuples or Django 3.0+ Choices class correctly
- No serializers (Django REST Framework not installed) - JSON endpoints will need manual serialization

### Important Notes

- French language throughout (UI, field names, comments)
- Status values are uppercase in models (EN_ATTENTE, VALIDE) but lowercase in template mock data (en_attente, valide)
- Settings.py: DEBUG=True, SECRET_KEY exposed, INSTALLED_APPS incomplete
- No API yet - templates are fully client-side with mock data

## File Reference Map

- [gestpers/settings.py](gestpers/settings.py) - Core Django config, INSTALLED_APPS location
- [gestpers/urls.py](gestpers/urls.py) - Root URL routing, app includes
- [Formation/models.py](Formation/models.py) - Formation and FormationStatus schema
- [Service/models.py](Service/models.py) - Service hierarchy and ServiceGerant schema
- [Userprofile/models.py](Userprofile/models.py) - Custom User model with avatar, groupe
- [template/soumissions.html](template/soumissions.html) - Key example of frontend pattern (tabbed tables, pagination, search, filtering)
- [Formation/views.py](Formation/views.py) - Current view handlers (render-only, no logic)

## Development Checklist

- [ ] Add Formation, Service, Userprofile to INSTALLED_APPS
- [ ] Fix TextChoices syntax in models (verify Django 5.2 syntax)
- [ ] Create missing Service and Userprofile views
- [ ] Implement API endpoints to replace template mock data
- [ ] Add DRF serializers for JSON responses
- [ ] Update templates to fetch real data via AJAX
- [ ] Write tests in app/tests.py files
