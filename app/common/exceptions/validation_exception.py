from fastapi import HTTPException, status
import logging as log

class ValidationRegisterException(HTTPException):
    def __init__(self, payload):
        errors = self.validate_payload(payload)
        if errors:
            log.error(errors)
            super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=errors)

    def validate_payload(self, payload):
        errors = []

        if not payload.name:
            log.error('Name is required')
            errors.append({'name': 'Name is required'})
        if not payload.email:
            log.error('Email is required')
            errors.append({'email': 'Email is required'})
        if not payload.password:
            log.error('Password is required')
            errors.append({'password': 'Password is required'})
        if not payload.passwordConfirm:
            log.error('Password Confirm is required')
            errors.append({'passwordConfirm': 'Password Confirm is required'})
        if payload.creator_id is not None and payload.creator_id != 0:
            log.error('Creator ID is not required')
            errors.append({'creator_id': 'Creator ID is not required'})
        if payload.password != payload.passwordConfirm:
            log.error('Passwords do not match')
            errors.append({'passwordConfirm': 'Passwords do not match'})
        if payload.password == 'string':
            log.error('Password is not valid (string)')
            errors.append({'password': 'Password is not valid (string)'})

        return errors

class ValidationLoginException(HTTPException):
    def __init__(self, payload):
        errors = self.validate_payload(payload)
        if errors:
            log.error(errors)
            super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=errors)

    def validate_payload(self, payload):
        errors = []

        if not payload.email:
            log.error('Email is required')
            errors.append({'email': 'Email is required'})
        if not payload.password:
            log.error('Password is required')
            errors.append({'password': 'Password is required'})
        if payload.password == 'string':
            log.error('Password is not valid (string)')
            errors.append({'password': 'Password is not valid (string)'})

        return errors