# File and Database Naming Conventions Guide

## Table of Contents
1. [General Principles](#general-principles)
2. [File System Naming](#file-system-naming)
3. [Source Code Files](#source-code-files)
4. [Database Objects](#database-objects)
5. [Media Files](#media-files)
6. [Documentation Files](#documentation-files)
7. [Version Control](#version-control)
8. [Special Characters](#special-characters)

## General Principles

### Universal Rules
- Use UTF-8 encoding for universal compatibility
- Maximum path length: 255 characters (POSIX standard)
- Maximum filename length: 255 bytes (POSIX standard)
- Avoid spaces in names
- Use lowercase as default (Unix/Linux standard)
- Avoid special characters except `-` and `_`
- Use ISO 8601 for date formats: YYYY-MM-DD

### Prohibited Characters
```
< > : " / \ | ? * [ ] & $ , ; = + % ' # @ ! ` ~ { } ( )
```

## File System Naming

### Directory Structure
```
project_name/
├── src/
├── docs/
├── tests/
├── build/
└── resources/
```

### Directory Naming
- Use lowercase
- Words separated by underscores
- Short but descriptive names
- Examples:
  ```
  user_data/
  system_logs/
  application_config/
  ```

## Source Code Files

### General Rules
- Use lowercase for filenames
- Extension must reflect language/purpose
- Include version number if necessary

### By Language
```
Python: example_module.py
Java: ExampleClass.java
JavaScript: example-component.js, example.service.js
C++: example_class.hpp, example_class.cpp
SQL: create_users_table.sql
```

### Configuration Files
```
config.yaml
.env.production
settings.json
```

## Database Objects

### Table Names
- Lowercase
- Plural form
- Underscores between words
- Examples:
  ```sql
  user_accounts
  product_categories
  order_items
  ```

### Column Names
- Lowercase
- Underscores between words
- No table name prefixes
- Examples:
  ```sql
  first_name
  last_login_date
  total_amount
  ```

### Index Names
Format: `idx_[table]_[column(s)]`
```sql
idx_users_email
idx_orders_created_at
```

### Foreign Keys
Format: `fk_[table]_[referenced_table]`
```sql
fk_order_items_products
fk_users_departments
```

## Media Files

### Images
Format: `[purpose]_[descriptor]_[dimensions].[extension]`
```
hero_landing_1920x1080.jpg
avatar_default_200x200.png
icon_settings_64x64.svg
```

### Audio
Format: `[type]_[descriptor]_[quality].[extension]`
```
podcast_episode1_192kbps.mp3
sfx_button_click_44k.wav
```

### Video
Format: `[project]_[scene]_[version].[extension]`
```
tutorial_intro_v2.mp4
promo_main_final.mov
```

## Documentation Files

### Technical Documentation
```
README.md
CHANGELOG.md
CONTRIBUTING.md
LICENSE.md
api_reference.md
```

### User Documentation
Format: `[product]_[version]_[document-type].[extension]`
```
system_v1.2_user_manual.pdf
api_v2_reference_guide.md
```

## Version Control

### Branch Names
Format: `[type]/[descriptor]`
```
feature/user-authentication
bugfix/login-error
hotfix/security-patch
```

### Tags
Format: `v[MAJOR].[MINOR].[PATCH]`
```
v1.0.0
v2.3.1
```

### Commit Messages
Format: `[type]: [description]`
```
feat: add user authentication
fix: resolve login error
docs: update API documentation
```

## Special Characters

### Allowed Special Characters
- Hyphen (`-`): For web-related files, URLs
- Underscore (`_`): Primary word separator
- Period (`.`): File extensions
- Forward slash (`/`): Directory separation

### Version Numbers
- Semantic Versioning: MAJOR.MINOR.PATCH
- Build Numbers: Build numbers should be numeric only
- Release Candidates: rc1, rc2, etc.

## Best Practices

## Case Usage Guidelines

### When to Use UPPERCASE
1. **Constants and Environment Variables**
   ```
   MAX_CONNECTIONS=100
   API_KEY="abc123"
   GLOBAL_TIMEOUT=30
   ```

2. **SQL Keywords (Convention)**
   ```sql
   SELECT * FROM users WHERE id = 1;
   CREATE TABLE products;
   ```

3. **Acronyms in Class Names**
   ```
   XMLParser
   APIController
   JSONResponse
   ```

### When to Use PascalCase (CapitalizedWords)
1. **Class Names (Most OOP Languages)**
   ```
   class UserAccount
   class DatabaseConnection
   class PaymentProcessor
   ```

2. **React/Angular Components**
   ```
   UserProfile.jsx
   NavigationBar.tsx
   LoginForm.component.ts
   ```

3. **Type Definitions (TypeScript)**
   ```typescript
   interface UserData
   type ApiResponse
   ```

### When to Use camelCase
1. **JavaScript/TypeScript Variables and Functions**
   ```javascript
   let firstName = "John"
   function calculateTotal()
   const getUserData = () => {}
   ```

2. **Java Methods and Variables**
   ```java
   public void processPayment()
   String userEmail;
   ```

3. **API Endpoint Parameters**
   ```
   /api/users?firstName=John&lastName=Doe
   ```

### When to Use snake_case (lowercase with underscores)
1. **Python Variables and Functions**
   ```python
   user_name = "John"
   def process_payment():
   ```

2. **Database Tables and Columns**
   ```sql
   user_accounts
   last_login_date
   ```

3. **Configuration Files**
   ```
   nginx_config.conf
   app_settings.json
   ```

### When to Use kebab-case (lowercase with hyphens)
1. **Web URLs and Domains**
   ```
   my-website-name.com
   about-us.html
   ```

2. **CSS Classes**
   ```css
   .nav-bar-item
   .header-logo
   ```

3. **npm Packages**
   ```
   react-router-dom
   @angular/core
   ```

### Special Case: Mixed Conventions
Some frameworks require specific mixed conventions:
1. **.NET Files**
   ```
   MyClass.cs (PascalCase)
   IMyInterface.cs (PascalCase with 'I' prefix)
   ```

2. **PHP Laravel**
   ```
   UserController.php (PascalCase)
   user_migration.php (snake_case)
   ```

### Case Sensitivity Rules by Environment
1. **Case-Sensitive**
   - Linux/Unix filesystems
   - Most programming language identifiers
   - Database objects in most DBMS
   
2. **Case-Insensitive**
   - Windows filesystem (by default)
   - SQL Server (by default)
   - macOS filesystem (by default)

### Date and Time
- Use ISO 8601 format
- File dates: YYYY-MM-DD
- Timestamps: YYYY-MM-DD_HH-MM-SS
- Time zones: Include UTC offset when necessary

### Temporary Files
Format: `[descriptor]_[timestamp]_tmp.[extension]`
```
backup_2024-03-15_tmp.sql
upload_2024-03-15_133022_tmp.dat
```

### Backup Files
Format: `[original-name]_[timestamp].bak`
```
database_2024-03-15_0300.bak
config_2024-03-15.bak
```

## References
- ISO/IEC 9945 POSIX
- ISO 8601 Date and Time Format
- RFC 2119 Requirement Levels
- Unicode Standard 15.1
- Semantic Versioning 2.0.0