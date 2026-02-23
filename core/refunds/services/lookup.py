"""Transaction lookup for refund research — FareGo + eTix + scan check."""

import logging
from datetime import timedelta
from decimal import Decimal

logger = logging.getLogger(__name__)

AMOUNT_BUFFER = Decimal("0.50")
DATE_BUFFER_DAYS = 1


class TransactionLookupService:
    """Search FareGo and eTix for original transactions."""

    @staticmethod
    def search(station_id=None, date=None, amount=None, device_id=None):
        """Search FareGo first, then eTix if not found."""
        results = {"farego": [], "etix": [], "source": None}

        farego = TransactionLookupService.search_farego(station_id, date, amount, device_id)
        results["farego"] = farego
        if farego:
            results["source"] = "farego"
            return results

        etix = TransactionLookupService.search_etix(station_id, date, amount)
        results["etix"] = etix
        if etix:
            results["source"] = "etix"
        return results

    @staticmethod
    def search_farego(station_id=None, date=None, amount=None, device_id=None):
        """Search revenue.SalesDetail (FareGo TVM data)."""
        from core.revenue.models import SalesDetail

        try:
            qs = SalesDetail.objects.all()
            if station_id:
                qs = qs.filter(dest_station_id=station_id)
            if date:
                from django.utils.dateparse import parse_date
                if isinstance(date, str):
                    date = parse_date(date)
                qs = qs.filter(
                    crea_date__date__gte=date - timedelta(days=DATE_BUFFER_DAYS),
                    crea_date__date__lte=date + timedelta(days=DATE_BUFFER_DAYS),
                )
            if amount:
                amount = Decimal(str(amount))
                qs = qs.filter(
                    fare_opt_amount__gte=amount - AMOUNT_BUFFER,
                    fare_opt_amount__lte=amount + AMOUNT_BUFFER,
                )
            if device_id:
                qs = qs.filter(device_id=device_id)
            qs = qs.filter(cancellation=False)
            return list(qs.order_by("-crea_date")[:50])
        except Exception as e:
            logger.error(f"FareGo search failed: {e}")
            return []

    @staticmethod
    def search_etix(station_id=None, date=None, amount=None):
        """Search ticket.ETixTicket (mobile app data)."""
        from core.ticket.models import ETixTicket

        try:
            from django.db.models import Q
            qs = ETixTicket.objects.all()
            if station_id:
                qs = qs.filter(Q(from_station_id=station_id) | Q(to_station_id=station_id))
            if date:
                from django.utils.dateparse import parse_date
                if isinstance(date, str):
                    date = parse_date(date)
                qs = qs.filter(
                    activate_start__date__gte=date - timedelta(days=DATE_BUFFER_DAYS),
                    activate_start__date__lte=date + timedelta(days=DATE_BUFFER_DAYS),
                )
            if amount:
                amount = Decimal(str(amount))
                qs = qs.filter(price__gte=amount - AMOUNT_BUFFER, price__lte=amount + AMOUNT_BUFFER)
            return list(qs.order_by("-activate_start")[:50])
        except Exception as e:
            logger.error(f"eTix search failed: {e}")
            return []

    @staticmethod
    def check_ticket_used(ticket):
        """Check if a ticket was scanned/used."""
        from core.ticket.models import TicketScan

        try:
            scans = list(TicketScan.objects.filter(ticket=ticket).order_by("-scanned_on"))
            return {"used": len(scans) > 0, "scan_count": len(scans), "scans": scans}
        except Exception as e:
            logger.error(f"Scan check failed: {e}")
            return {"used": False, "scan_count": 0, "scans": []}

    @staticmethod
    def get_sales_detail_key(sales_detail):
        """Extract composite key from SalesDetail for linking to RefundTicket."""
        return {
            "device_id": sales_detail.device_id,
            "device_class_id": sales_detail.device_class_id,
            "sales_detail_ev_sequ_no": sales_detail.sales_detail_ev_sequ_no,
            "sales_transaction_no": sales_detail.sales_transaction_no,
            "unique_ms_id": sales_detail.unique_ms_id,
            "correction_counter": sales_detail.correction_counter,
        }
