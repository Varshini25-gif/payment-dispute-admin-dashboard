import pandas as pd

from app.components.tables import filter_disputes, generate_sample_disputes, paginate_dataframe


class TestDisputeTableHelpers:
    def test_generate_sample_disputes_returns_expected_schema(self):
        data = generate_sample_disputes(5)

        assert len(data) == 5
        expected_columns = {
            "Dispute ID",
            "Customer",
            "Status",
            "Priority",
            "Amount",
            "Created",
            "Reason",
            "Assigned To",
        }
        assert expected_columns.issubset(set(data.columns))

    def test_filter_disputes_applies_search_status_and_priority(self):
        data = pd.DataFrame(
            [
                {
                    "Dispute ID": "DIS-1001",
                    "Customer": "Acme Corp",
                    "Status": "Pending",
                    "Priority": "High",
                    "Amount": "$500.00",
                    "Created": "2026-05-20",
                    "Reason": "Chargeback dispute",
                    "Assigned To": "Jordan",
                },
                {
                    "Dispute ID": "DIS-1002",
                    "Customer": "Globex",
                    "Status": "Resolved",
                    "Priority": "Low",
                    "Amount": "$250.00",
                    "Created": "2026-05-21",
                    "Reason": "Refund mismatch",
                    "Assigned To": "Taylor",
                },
                {
                    "Dispute ID": "DIS-2001",
                    "Customer": "Acme Finance",
                    "Status": "Pending",
                    "Priority": "High",
                    "Amount": "$800.00",
                    "Created": "2026-05-22",
                    "Reason": "Duplicate charge",
                    "Assigned To": "Morgan",
                },
            ]
        )

        filtered = filter_disputes(
            data,
            search_term="acme",
            status="Pending",
            priority="High",
        )

        assert len(filtered) == 2
        assert filtered["Status"].tolist() == ["Pending", "Pending"]
        assert filtered["Priority"].tolist() == ["High", "High"]
        assert filtered["Customer"].tolist() == ["Acme Corp", "Acme Finance"]

    def test_paginate_dataframe_returns_expected_slice(self):
        data = pd.DataFrame({"Dispute ID": [f"DIS-{i:04d}" for i in range(1, 21)]})

        page, meta = paginate_dataframe(data, page_index=2, page_size=5)

        assert page["Dispute ID"].tolist() == ["DIS-0006", "DIS-0007", "DIS-0008", "DIS-0009", "DIS-0010"]
        assert meta["page_index"] == 2
        assert meta["page_size"] == 5
        assert meta["total_rows"] == 20
        assert meta["total_pages"] == 4
        assert meta["has_prev"] is True
        assert meta["has_next"] is True
