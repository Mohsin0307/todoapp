# Data Model: Advanced Cloud Deployment Todo Chatbot

## Overview
This document defines the data models for the event-driven Todo Chatbot application, including entities for advanced features like recurring tasks, notifications, and event tracking.

## Core Entities

### 1. User
**Purpose**: Represents system users with authentication details and preferences

```python
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column(String, unique=True, index=True))
    password_hash: str
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())
    preferences: dict | None = Field(default={})
    last_login: datetime | None = None
    is_active: bool = True
```

**Relationships**:
- One-to-Many: User -> TodoItem
- One-to-Many: User -> Notification
- One-to-Many: User -> EventLog

### 2. TodoItem
**Purpose**: Represents a task to be completed with advanced features

```python
class TodoItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(String, nullable=False))
    description: str | None = Field(default=None)
    status: str = Field(default="pending", sa_column=Column(String, nullable=False))  # pending, in_progress, completed, cancelled
    priority: str = Field(default="medium", sa_column=Column(String, nullable=False))  # low, medium, high, urgent
    due_date: datetime | None = None
    user_id: int = Field(foreign_key="user.id")

    # Advanced features
    tags: list[str] | None = Field(default=[])
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())

    # Recurrence
    is_recurring: bool = False
    recurrence_pattern: str | None = Field(default=None)  # daily, weekly, monthly, yearly
    recurrence_interval: int | None = Field(default=None)  # e.g., every 2 weeks
    recurrence_end_date: datetime | None = None

    # Reminders
    reminder_enabled: bool = False
    reminder_time: datetime | None = None
    reminder_offset_hours: int | None = Field(default=None)  # Hours before due_date

    # Dependencies
    parent_id: int | None = Field(default=None, foreign_key="todoitem.id")  # For hierarchical tasks
    depends_on_ids: list[int] | None = Field(default=[])  # IDs this task depends on
```

**Validation Rules**:
- Title must not be empty
- Status must be one of allowed values
- Priority must be one of allowed values
- Due date must be in the future if set
- Recurrence pattern requires interval if set

### 3. Event
**Purpose**: Represents events in the system processed through event streams

```python
class Event(SQLModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str = Field(sa_column=Column(String, nullable=False))  # todo.created, todo.updated, todo.completed, reminder.triggered
    source: str = Field(sa_column=Column(String, nullable=False))  # service that generated the event
    timestamp: datetime = Field(default=datetime.utcnow())
    correlation_id: str | None = Field(default_factory=lambda: str(uuid.uuid4()))
    causation_id: str | None = None  # ID of the event that caused this event
    payload: dict = Field(default={})  # Event-specific data
    user_id: int | None = None  # Associated user
    todo_id: int | None = None  # Associated todo item
    processed: bool = False  # Whether event has been consumed by all interested services
    retries: int = 0  # Number of retry attempts
    max_retries: int = 3  # Maximum number of retries before dead-lettering
```

**Event Types**:
- `todo.created`: When a new todo item is created
- `todo.updated`: When a todo item is modified
- `todo.completed`: When a todo item is marked as completed
- `todo.deleted`: When a todo item is deleted
- `todo.recurring.triggered`: When a recurring todo is triggered
- `reminder.sent`: When a reminder is sent to a user
- `notification.created`: When a new notification is generated

### 4. Notification
**Purpose**: Represents alerts sent to users for reminders and system events

```python
class Notification(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    type: str = Field(sa_column=Column(String, nullable=False))  # reminder, system, alert
    title: str = Field(sa_column=Column(String, nullable=False))
    message: str = Field(sa_column=Column(Text, nullable=False))
    priority: str = Field(default="normal", sa_column=Column(String, nullable=False))  # low, normal, high, urgent
    target_users: list[int] | None = Field(default=[])  # For broadcast notifications
    created_at: datetime = Field(default=datetime.utcnow())
    scheduled_for: datetime | None = None  # When notification should be delivered
    sent_at: datetime | None = None  # When notification was actually sent
    read_at: datetime | None = None  # When notification was read by user
    is_read: bool = False
    is_delivered: bool = False
    delivery_method: str = Field(default="in_app", sa_column=Column(String, nullable=False))  # in_app, email, sms, push
    todo_id: int | None = Field(foreign_key="todoitem.id")  # Associated todo item
    event_id: str | None = Field(foreign_key="event.id")  # Associated event
```

### 5. RecurringPattern
**Purpose**: Defines recurring task patterns that can be reused

```python
class RecurringPattern(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String, unique=True, nullable=False))
    pattern_type: str = Field(sa_column=Column(String, nullable=False))  # daily, weekly, monthly, yearly, custom
    interval: int = Field(default=1)  # e.g., every 2 days/weeks/months
    day_of_week: int | None = Field(default=None, ge=0, le=6)  # 0=Monday, 6=Sunday
    day_of_month: int | None = Field(default=None, ge=1, le=31)  # Day of month (1-31)
    month: int | None = Field(default=None, ge=1, le=12)  # Month (1-12)
    time_of_day: time | None = Field(default=time(9, 0))  # Time of day for recurring tasks
    created_by: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())
    is_active: bool = True
```

## Dapr Components

### 1. PubSub Component (Kafka/Redpanda)
**Purpose**: Event streaming for distributed communication

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: todo-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "localhost:9092" # For local, will be replaced in production
  - name: authRequired
    value: "false" # For local development, true in production
  - name: consumerGroup
    value: "todo-consumer-group"
```

### 2. State Store Component
**Purpose**: Distributed state management

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: todo-statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: "localhost:6379"
  - name: redisPassword
    secretKeyRef:
      name: redis-password
      key: redis-password
```

### 3. Secret Store Component
**Purpose**: Secure management of secrets

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: todo-secretstore
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
```

## Relationships and Constraints

### TodoItem Relationships
```
User (1) -- (Many) TodoItem (1) -- (Many) Notification
                    |
                    | (Many) Event
                    |
                    | (1) Parent TodoItem
```

### Event Relationships
```
Event (Many) -- (1) User
Event (Many) -- (1) TodoItem
Event (Many) -- (1) Notification
```

## Indexing Strategy

### Critical Indices
1. `TodoItem.user_id` - For user-specific queries
2. `TodoItem.status` - For status-based filtering
3. `TodoItem.due_date` - For due date sorting and filtering
4. `TodoItem.priority` - For priority-based queries
5. `TodoItem.tags` - For tag-based searching (GIN index if PostgreSQL supports)
6. `Notification.user_id` - For user-specific notifications
7. `Notification.created_at` - For chronological retrieval
8. `Event.type` - For event-type based querying
9. `Event.timestamp` - For temporal queries
10. `Event.processed` - For event processing state

## State Transitions

### TodoItem State Transitions
```
pending -> in_progress -> completed
     |-> cancelled
```

### Notification State Transitions
```
created -> scheduled -> sent -> read
                |
                +-> delivered
```

### Event Processing States
```
created -> processing -> processed
                    |
                    +-> failed -> retried -> processed
                                    |
                                    +-> dead_lettered
```

## Validation Rules

### TodoItem
- Title length: 1-255 characters
- Description length: 0-2000 characters
- Status: One of ["pending", "in_progress", "completed", "cancelled"]
- Priority: One of ["low", "medium", "high", "urgent"]
- Due date must be in the future when setting
- Tags length: Max 10 tags, each 1-50 characters
- Recurrence pattern requires interval and/or end condition

### User
- Email: Valid email format
- Password: Minimum 8 characters, complex requirements
- Created/updated timestamps auto-managed

### Event
- Type: Predefined set of valid event types
- Payload: Must conform to event-specific schema
- Retry count: Max 3 attempts before dead-lettering
- Timestamps: Immutable after creation

### Notification
- Type: One of ["reminder", "system", "alert"]
- Priority: One of ["low", "normal", "high", "urgent"]
- Delivery method: One of ["in_app", "email", "sms", "push"]

## Audit Trail
All entities include `created_at`, `updated_at`, and `updated_by` fields for auditability. Event logs maintain complete change history through event sourcing patterns.