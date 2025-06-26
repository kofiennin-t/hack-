# Entity Relationship Diagram (ERD)
## AI Model Platform Database Schema

### Entity Overview
The database consists of 6 main entities with the following relationships:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AI MODEL PLATFORM ERD                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐              ┌──────────────────┐
│      USERS       │              │   DEVELOPERS     │
│                  │              │                  │
│ PK: user_id      │              │ PK: developer_id │
│    username      │              │    username      │
│    email         │              │    email         │
│    password_hash │              │    password_hash │
│    first_name    │              │    first_name    │
│    last_name     │              │    last_name     │
│    phone_number  │              │    company_name  │
│    country       │              │    website_url   │
│    city          │              │    github_profile│
│    profile_pic   │              │    expertise[]   │
│    bio           │              │    years_exp     │
│    status        │              │    api_quota     │
│    email_verified│              │    total_models  │
│    created_at    │              │    status        │
│    updated_at    │              │    created_at    │
└──────────────────┘              └──────────────────┘
         │                                   │
         │                                   │ 1
         │                                   │
         │ 1                                 │
         │                          ┌───────▼──────────┐
         │                          │     MODELS       │
         │                          │                  │
         │                          │ PK: model_id     │
         │                          │ FK: developer_id │
         │                          │    model_name    │
         │                          │    display_name  │
         │                          │    description   │
         │                          │    api_name      │
         │                          │    api_key       │
         │                          │    category      │
         │                          │    tags[]        │
         │                          │    status        │
         │                          │    total_requests│
         │                          │    avg_rating    │
         │                          │    created_at    │
         │                          └───────┬──────────┘
         │                                  │ 1
         │                                  │
         │                                  │
         │ *                                │ *
┌────────▼──────────┐              ┌───────▼──────────┐
│  USER_HISTORY     │              │  MODEL_REVIEWS   │
│                   │              │                  │
│ PK: history_id    │              │ PK: review_id    │
│ FK: user_id       │              │ FK: model_id     │
│ FK: model_id      │              │ FK: user_id      │
│    session_id     │              │    rating        │
│    prompt         │              │    review_title  │
│    response       │              │    review_text   │
│    status         │              │    helpful_votes │
│    timestamp      │              │    created_at    │
│    response_time  │              └──────────────────┘
│    cost_incurred  │                        │
│    user_rating    │                        │ *
│    ip_address     │                        │
│    created_at     │               ┌────────▼──────────┐
└───────────────────┘               │  API_USAGE_LOGS   │
                                    │                   │
                                    │ PK: log_id        │
                                    │ FK: user_id       │
                                    │ FK: developer_id  │
                                    │ FK: model_id      │
                                    │    api_key_used   │
                                    │    request_method │
                                    │    response_code  │
                                    │    request_size   │
                                    │    response_size  │
                                    │    processing_time│
                                    │    created_at     │
                                    └───────────────────┘
```

### Detailed Relationships

#### 1. USERS Entity
- **Primary Key**: `user_id` (UUID)
- **Unique Constraints**: `username`, `email`
- **Status Enum**: active, inactive, suspended, pending_verification

#### 2. DEVELOPERS Entity
- **Primary Key**: `developer_id` (UUID)
- **Unique Constraints**: `username`, `email`
- **Status Enum**: active, inactive, suspended, pending_approval
- **Array Fields**: `expertise_areas[]`

#### 3. MODELS Entity
- **Primary Key**: `model_id` (UUID)
- **Foreign Key**: `developer_id` → DEVELOPERS(developer_id)
- **Unique Constraints**: `api_name`, `api_key`
- **Category Enum**: text_generation, image_generation, code_generation, etc.
- **Status Enum**: active, inactive, under_review, deprecated
- **Array Fields**: `tags[]`

#### 4. USER_HISTORY Entity
- **Primary Key**: `history_id` (UUID)
- **Foreign Keys**: 
  - `user_id` → USERS(user_id)
  - `model_id` → MODELS(model_id)
- **Composite Business Key**: `user_id`, `session_id`, `request_timestamp`

#### 5. MODEL_REVIEWS Entity
- **Primary Key**: `review_id` (UUID)
- **Foreign Keys**:
  - `model_id` → MODELS(model_id)
  - `user_id` → USERS(user_id)
- **Unique Constraint**: `(model_id, user_id)` - One review per user per model

#### 6. API_USAGE_LOGS Entity
- **Primary Key**: `log_id` (UUID)
- **Foreign Keys**:
  - `user_id` → USERS(user_id) [nullable]
  - `developer_id` → DEVELOPERS(developer_id) [nullable]
  - `model_id` → MODELS(model_id)

### Relationship Cardinalities

1. **DEVELOPERS → MODELS**: One-to-Many (1:*)
   - One developer can create multiple models
   - Each model belongs to exactly one developer

2. **USERS → USER_HISTORY**: One-to-Many (1:*)
   - One user can have multiple interaction history records
   - Each history record belongs to exactly one user

3. **MODELS → USER_HISTORY**: One-to-Many (1:*)
   - One model can have multiple user interactions
   - Each interaction uses exactly one model

4. **USERS → MODEL_REVIEWS**: One-to-Many (1:*)
   - One user can write multiple reviews
   - Each review is written by exactly one user

5. **MODELS → MODEL_REVIEWS**: One-to-Many (1:*)
   - One model can have multiple reviews
   - Each review is for exactly one model

6. **MODELS → API_USAGE_LOGS**: One-to-Many (1:*)
   - One model can have multiple API usage logs
   - Each log entry is for exactly one model

### Key Business Rules

1. **User-Model Interaction**: Users interact with models through the USER_HISTORY table
2. **Review Uniqueness**: Each user can only review a specific model once
3. **Developer Ownership**: Models are owned by developers and cannot exist without a developer
4. **Cascade Deletes**: Deleting a user/developer/model cascades to related records
5. **Status Management**: Both users and developers have status management for access control
6. **API Rate Limiting**: Developers have quota limits tracked in the API usage logs

### Views Created

1. **public_models_view**: Shows all active public models with developer info
2. **user_activity_summary**: Aggregated user activity statistics
3. **developer_dashboard_stats**: Developer performance and revenue metrics

### Triggers and Automation

1. **Auto-update timestamps**: `updated_at` fields automatically maintained
2. **Model count tracking**: Developer's `total_models_created` auto-updated
3. **Rating calculations**: Model `average_rating` and `rating_count` auto-calculated
4. **Usage statistics**: Model `total_requests` and `total_users` auto-updated
