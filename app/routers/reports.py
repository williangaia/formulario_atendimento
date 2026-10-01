import csv
import io
from datetime import datetime

import pandas as pd
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.form_answers import FormAnswers
from app.models.stores import Store
from app.templating import templates

router = APIRouter()

def build_report_rows(rows):
    report_rows = []

    for answer, store in rows:
        created_at = answer.created_at

        report_rows.append(
            {
                "LOJA": store.name,
                "NROEMPRESA": store.nroempresa,
                "DATA": created_at.strftime("%d/%m/%Y"),
                "HORÁRIO": created_at.strftime("%H:%M"),
                "RUIM": 1 if answer.answer == "ruim" else "",
                "BOM": 1 if answer.answer == "bom" else "",
                "EXCELENTE": 1 if answer.answer == "excelente" else "",
            }
        )  

    return report_rows

async def fetch_report_rows(
    db: AsyncSession,
):
    result = await db.execute(
        select(FormAnswers, Store)
        .join(Store, Store.id == FormAnswers.store_id)
        .order_by(FormAnswers.created_at)
    )

    return result.all()

@router.get(
    path="/relatorios",
    status_code=status.HTTP_200_OK,
    summary="Tela onde os arquivos dos relatórios podem ser baixados"
)
async def reports_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="reports.html",
    )

@router.get(
    path="/relatorios/satisfacao.csv",
    status_code=status.HTTP_200_OK,
    summary="Criar o arquivo com as repostas do formulário em formato csv",
)
async def download_csv(
    db: AsyncSession = Depends(get_session),
):
    rows = await fetch_report_rows(db)
    report_rows = build_report_rows(rows)

    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "LOJA",
            "NROEMPRESA",
            "DATA",
            "HORÁRIO",
            "RUIM",
            "BOM",
            "EXCELENTE",
        ],
        delimiter=";",
    )

    writer.writeheader()
    writer.writerows(report_rows)

    content = output.getvalue().encode("utf-8-sig")

    return StreamingResponse(
        io.BytesIO(content),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                "attachment; "
                'filename="relatorio_formulario.csv"'
            )
        },
    )

@router.get(
    path="/relatorios/satisfacao.xlsx",
    status_code=status.HTTP_200_OK,
    summary="Criar o arquivo com as repostas do formulário em formato xlsx",
    )
async def download_xlsx(
    db: AsyncSession = Depends(get_session),
):
    rows = await fetch_report_rows(db)
    report_rows = build_report_rows(rows)

    dataframe = pd.DataFrame(
        report_rows,
        columns=[
            "LOJA",
            "NROEMPRESA",
            "DATA",
            "HORÁRIO",
            "RUIM",
            "BOM",
            "EXCELENTE",
        ],
    )

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl",
    ) as writer:
        dataframe.to_excel(
            writer,
            sheet_name="Respostas",
            index=False,
        )

        worksheet = writer.sheets["Respostas"]
        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions

        widths = {
            "A": 22,
            "B": 14,
            "C": 14,
            "D": 12,
            "E": 12,
            "F": 12,
            "G": 14,
        }

        for column, width in widths.items():
            worksheet.column_dimensions[column].width = width

    output.seek(0)

    return StreamingResponse(
        output,
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition": (
                "attachment; "
                'filename="relatorio_formulario.xlsx"'
            )
        },
    )