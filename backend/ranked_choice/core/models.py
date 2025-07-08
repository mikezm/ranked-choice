from django.db import models


class Ballot(models.Model):
    """
    Ballot model for storing ballot information.
    Uses an auto-incrementing integer primary key,
    timestamps, and includes slug and title fields.
    """
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'core'
        db_table = 'ballots'

    def __str__(self):
        return self.title


class Choice(models.Model):
    """
    Choice model for storing ballot choices.
    Has a foreign key to the Ballot model, a required name field,
    and an optional description field.
    """
    id = models.AutoField(primary_key=True)
    ballot = models.ForeignKey(
        Ballot,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'core'
        db_table = 'choices'

    def __str__(self):
        return self.name


class Voter(models.Model):
    """
    Voter model for storing voter information.
    """
    id = models.AutoField(primary_key=True)
    ballot = models.ForeignKey(
        Ballot,
        on_delete=models.CASCADE,
        related_name='voters'
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'core'
        db_table = 'voters'

    def __str__(self):
        return self.name


class Vote(models.Model):
    """
    Votes model for storing votes.
    """
    id = models.AutoField(primary_key=True)
    voter = models.ForeignKey(
        Voter,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    rank = models.PositiveIntegerField()
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'core'
        db_table = 'votes'

    def __str__(self):
        return f"Vote for {self.choice.name} by {self.voter.name}"