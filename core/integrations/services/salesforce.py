"""SalesForce service for Case, Contact, and Comment operations."""

import logging

from core.integrations.contrib.salesforce import SalesForceClient

logger = logging.getLogger(__name__)


class SalesForceService:
    """Shared SalesForce API operations for all CORE apps."""

    # ── Cases ──────────────────────────────────

    @staticmethod
    def get_case(sf_id):
        """Pull a single case from SalesForce."""
        sf = SalesForceClient.get_connection()
        if not sf:
            return None
        try:
            result = sf.query(
                "SELECT Id, Subject, Status, Description, "
                "ContactId, Contact.Name, Contact.Email, "
                "Case_Record_Type_Text__c, RecordType__c, "
                "CreatedDate, LastModifiedDate "
                f"FROM Case WHERE Id = '{sf_id}'"
            )
            if result["totalSize"] > 0:
                return result["records"][0]
        except Exception as e:
            logger.error(f"get_case failed for {sf_id}: {e}")
        return None

    @staticmethod
    def get_cases(record_type=None, status=None, limit=100, offset=0):
        """Pull a filtered list of cases for the dashboard."""
        sf = SalesForceClient.get_connection()
        if not sf:
            return []
        try:
            query = (
                "SELECT Id, Subject, Status, Contact.Name, "
                "Case_Record_Type_Text__c, CreatedDate, LastModifiedDate "
                "FROM Case"
            )
            where = []
            if record_type:
                where.append(f"Case_Record_Type_Text__c = '{record_type}'")
            if status:
                where.append(f"Status = '{status}'")
            if where:
                query += " WHERE " + " AND ".join(where)
            query += f" ORDER BY LastModifiedDate DESC LIMIT {limit} OFFSET {offset}"
            result = sf.query(query)
            return result.get("records", [])
        except Exception as e:
            logger.error(f"get_cases failed: {e}")
        return []

    @staticmethod
    def create_case(subject, description="", record_type="", contact_sf_id=None):
        """Create a new case in SalesForce. Returns sf_id or None."""
        sf = SalesForceClient.get_connection()
        if not sf:
            return None
        try:
            data = {"Subject": subject, "Description": description, "Status": "Received"}
            if record_type:
                data["Case_Record_Type_Text__c"] = record_type
            if contact_sf_id:
                data["ContactId"] = contact_sf_id
            result = sf.Case.create(data)
            sf_id = result.get("id")
            logger.info(f"Case created: {sf_id}")
            return sf_id
        except Exception as e:
            logger.error(f"create_case failed: {e}")
        return None

    @staticmethod
    def update_case(sf_id, fields):
        """Update fields on a SalesForce case."""
        sf = SalesForceClient.get_connection()
        if not sf:
            return False
        try:
            sf.Case.update(sf_id, fields)
            logger.info(f"Case updated: {sf_id}")
            return True
        except Exception as e:
            logger.error(f"update_case failed for {sf_id}: {e}")
        return False

    @staticmethod
    def update_case_status(sf_id, status, status_detail=None):
        """Update case status and optional detail."""
        fields = {"Status": status}
        if status_detail:
            fields["Status_Detail__c"] = status_detail
        return SalesForceService.update_case(sf_id, fields)

    # ── Comments ───────────────────────────────

    @staticmethod
    def add_comment(sf_id, body, is_public=False):
        """Add a comment to a case's activity history."""
        sf = SalesForceClient.get_connection()
        if not sf:
            return None
        try:
            result = sf.CaseComment.create(
                {"ParentId": sf_id, "CommentBody": body, "IsPublished": is_public}
            )
            return result.get("id")
        except Exception as e:
            logger.error(f"add_comment failed for {sf_id}: {e}")
        return None

    @staticmethod
    def get_comments(sf_id):
        """Pull all comments for a case."""
        sf = SalesForceClient.get_connection()
        if not sf:
            return []
        try:
            result = sf.query(
                "SELECT Id, CommentBody, CreatedDate, CreatedBy.Name, IsPublished "
                f"FROM CaseComment WHERE ParentId = '{sf_id}' "
                "ORDER BY CreatedDate DESC"
            )
            return result.get("records", [])
        except Exception as e:
            logger.error(f"get_comments failed for {sf_id}: {e}")
        return []

    # ── Contacts ───────────────────────────────

    @staticmethod
    def get_contact(contact_sf_id):
        """Pull a single contact from SalesForce."""
        sf = SalesForceClient.get_connection()
        if not sf:
            return None
        try:
            result = sf.query(
                "SELECT Id, Name, FirstName, LastName, Email, Phone, MailingAddress "
                f"FROM Contact WHERE Id = '{contact_sf_id}'"
            )
            if result["totalSize"] > 0:
                return result["records"][0]
        except Exception as e:
            logger.error(f"get_contact failed for {contact_sf_id}: {e}")
        return None

    @staticmethod
    def search_contacts(term):
        """Search contacts by name or email (SounDex supported)."""
        sf = SalesForceClient.get_connection()
        if not sf:
            return []
        try:
            result = sf.search(
                f"FIND {{{term}}} IN ALL FIELDS "
                "RETURNING Contact(Id, Name, Email, Phone)"
            )
            return result.get("searchRecords", [])
        except Exception as e:
            logger.error(f"search_contacts failed for '{term}': {e}")
        return []

    # ── Utility ────────────────────────────────

    @staticmethod
    def is_connected():
        """Check if SalesForce connection is active."""
        return SalesForceClient.get_connection() is not None
