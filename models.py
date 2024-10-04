# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('PO', 'Project Owner'),
        ('MG', 'Manager'),
        ('FP', 'Finance Personnel'),
        ('OC', 'Oversight Committee'),
    ]
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)


class ExpenditureRequest(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('IN_REVIEW', 'In Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    scope = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]


class ApprovalWorkflowStep(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField()
    required_role = models.CharField(max_length=2, choices=User.ROLE_CHOICES)

    class Meta:
        ordering = ['order']
        unique_together = ['order', 'required_role']


class Approval(models.Model):
    expenditure_request = models.ForeignKey(ExpenditureRequest, on_delete=models.CASCADE, related_name='approvals')
    workflow_step = models.ForeignKey(ApprovalWorkflowStep, on_delete=models.CASCADE)
    approver = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField()
    comments = models.TextField(blank=True)
    approved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['expenditure_request', 'workflow_step', 'approver']
        indexes = [
            models.Index(fields=['expenditure_request', 'workflow_step']),
        ]
