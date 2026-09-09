from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Absenteeism_at_work.csv"

RENAME_COLUMNS = {
    "ID": "id_colaborador",
    "Reason for absence": "motivo_ausencia",
    "Month of absence": "mes_ausencia",
    "Day of the week": "dia_semana",
    "Seasons": "estacao",
    "Transportation expense": "custo_transporte",
    "Distance from Residence to Work": "distancia_casa_trabalho",
    "Service time": "tempo_servico",
    "Age": "idade",
    "Work load Average/day ": "carga_trabalho_media_dia",
    "Hit target": "meta_atingida",
    "Disciplinary failure": "falha_disciplinar",
    "Education": "educacao",
    "Son": "filhos",
    "Social drinker": "consome_alcool",
    "Social smoker": "fumante",
    "Pet": "pets",
    "Weight": "peso",
    "Height": "altura",
    "Body mass index": "imc",
    "Absenteeism time in hours": "horas_absenteismo",
}

SEASONS = {1: "Primavera", 2: "Verão", 3: "Outono", 4: "Inverno"}
MONTHS = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}
EDUCATION = {1: "Ensino médio", 2: "Graduação", 3: "Pós-graduação", 4: "Mestrado/doutorado"}
YES_NO = {0: "Não", 1: "Sim"}


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Arquivo de dados não encontrado: {DATA_PATH}")

    data = pd.read_csv(DATA_PATH, sep=";").rename(columns=RENAME_COLUMNS)
    data["estacao_nome"] = data["estacao"].map(SEASONS).fillna("Não informado")
    data["mes_nome"] = data["mes_ausencia"].map(MONTHS).fillna("Não informado")
    data["educacao_nome"] = data["educacao"].map(EDUCATION).fillna("Não informado")
    data["consome_alcool_nome"] = data["consome_alcool"].map(YES_NO)
    data["fumante_nome"] = data["fumante"].map(YES_NO)
    data["flag_absenteismo"] = data["horas_absenteismo"].gt(0)
    return data


def format_number(value: float) -> str:
    return f"{value:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")


def build_filters(data: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filtros da análise")
    st.sidebar.caption("Use os filtros para recortar a visão gerencial.")

    months = st.sidebar.multiselect(
        "Mês da ausência",
        options=list(MONTHS.values()),
        default=list(MONTHS.values()),
    )
    seasons = st.sidebar.multiselect(
        "Estação do ano",
        options=list(SEASONS.values()),
        default=list(SEASONS.values()),
    )
    education = st.sidebar.multiselect(
        "Escolaridade",
        options=list(EDUCATION.values()),
        default=list(EDUCATION.values()),
    )
    alcohol = st.sidebar.multiselect(
        "Consumo de álcool",
        options=list(YES_NO.values()),
        default=list(YES_NO.values()),
    )
    smoker = st.sidebar.multiselect(
        "Tabagismo",
        options=list(YES_NO.values()),
        default=list(YES_NO.values()),
    )
    age_range = st.sidebar.slider(
        "Faixa etária",
        min_value=int(data["idade"].min()),
        max_value=int(data["idade"].max()),
        value=(int(data["idade"].min()), int(data["idade"].max())),
    )

    filtered = data[
        data["mes_nome"].isin(months)
        & data["estacao_nome"].isin(seasons)
        & data["educacao_nome"].isin(education)
        & data["consome_alcool_nome"].isin(alcohol)
        & data["fumante_nome"].isin(smoker)
        & data["idade"].between(*age_range)
    ].copy()

    st.sidebar.divider()
    st.sidebar.metric("Registros filtrados", f"{len(filtered):,}".replace(",", "."))
    return filtered


def render_kpis(data: pd.DataFrame) -> None:
    total_records = len(data)
    total_hours = data["horas_absenteismo"].sum()
    average_hours = data["horas_absenteismo"].mean() if total_records else 0
    affected_people = data.loc[data["flag_absenteismo"], "id_colaborador"].nunique()

    columns = st.columns(4)
    columns[0].metric("Registros de ausência", f"{total_records:,}".replace(",", "."))
    columns[1].metric("Horas de absenteísmo", format_number(total_hours))
    columns[2].metric("Média por registro", f"{format_number(average_hours)} h")
    columns[3].metric("Colaboradores envolvidos", f"{affected_people:,}".replace(",", "."))


def render_overview(data: pd.DataFrame) -> None:
    st.subheader("Visão executiva")
    render_kpis(data)

    if data.empty:
        st.warning("Nenhum registro corresponde aos filtros selecionados.")
        return

    left, right = st.columns(2)
    by_month = (
        data.groupby(["mes_ausencia", "mes_nome"], as_index=False)["horas_absenteismo"]
        .sum()
        .sort_values("mes_ausencia")
    )
    monthly_chart = px.bar(
        by_month,
        x="mes_nome",
        y="horas_absenteismo",
        labels={"mes_nome": "Mês", "horas_absenteismo": "Horas"},
        title="Horas de absenteísmo por mês",
        color="horas_absenteismo",
        color_continuous_scale="Blues",
    )
    monthly_chart.update_layout(showlegend=False, coloraxis_showscale=False)
    left.plotly_chart(monthly_chart, use_container_width=True)

    reasons = (
        data.groupby("motivo_ausencia", as_index=False)
        .agg(registros=("motivo_ausencia", "size"), horas=("horas_absenteismo", "sum"))
        .sort_values("registros", ascending=False)
        .head(10)
    )
    reason_chart = px.bar(
        reasons.sort_values("registros"),
        x="registros",
        y="motivo_ausencia",
        orientation="h",
        labels={"motivo_ausencia": "Código do motivo", "registros": "Registros"},
        title="10 motivos mais frequentes",
        color="registros",
        color_continuous_scale="Teal",
    )
    reason_chart.update_layout(showlegend=False, coloraxis_showscale=False)
    right.plotly_chart(reason_chart, use_container_width=True)

    st.markdown(
        "**Leitura para decisão:** o painel consolida os indicadores de frequência e duração "
        "para apoiar a priorização de ações de saúde ocupacional, transporte e gestão de pessoas."
    )


def render_profile(data: pd.DataFrame) -> None:
    st.subheader("Perfil dos colaboradores")
    if data.empty:
        st.info("Selecione filtros que retornem registros para visualizar o perfil.")
        return

    left, right = st.columns(2)
    age_chart = px.histogram(
        data,
        x="idade",
        nbins=15,
        labels={"idade": "Idade", "count": "Registros"},
        title="Distribuição etária",
        color_discrete_sequence=["#2563eb"],
    )
    left.plotly_chart(age_chart, use_container_width=True)

    bmi_chart = px.scatter(
        data,
        x="imc",
        y="horas_absenteismo",
        color="consome_alcool_nome",
        hover_data=["idade", "distancia_casa_trabalho"],
        labels={
            "imc": "IMC",
            "horas_absenteismo": "Horas de absenteísmo",
            "consome_alcool_nome": "Consome álcool",
        },
        title="IMC x horas de absenteísmo",
    )
    right.plotly_chart(bmi_chart, use_container_width=True)

    profile = (
        data.groupby("educacao_nome", as_index=False)
        .agg(registros=("id_colaborador", "size"), horas=("horas_absenteismo", "sum"))
        .sort_values("horas", ascending=False)
    )
    education_chart = px.bar(
        profile,
        x="educacao_nome",
        y="horas",
        labels={"educacao_nome": "Escolaridade", "horas": "Horas"},
        title="Horas por escolaridade",
        color="educacao_nome",
    )
    education_chart.update_layout(showlegend=False)
    st.plotly_chart(education_chart, use_container_width=True)


def render_factors(data: pd.DataFrame) -> None:
    st.subheader("Fatores associados ao absenteísmo")
    if data.empty:
        st.info("Selecione filtros que retornem registros para visualizar os fatores.")
        return

    left, right = st.columns(2)
    distance_chart = px.scatter(
        data,
        x="distancia_casa_trabalho",
        y="horas_absenteismo",
        size="custo_transporte",
        color="estacao_nome",
        hover_data=["idade", "tempo_servico"],
        labels={
            "distancia_casa_trabalho": "Distância (km)",
            "horas_absenteismo": "Horas",
            "custo_transporte": "Custo de transporte",
            "estacao_nome": "Estação",
        },
        title="Distância casa-trabalho x horas de ausência",
    )
    left.plotly_chart(distance_chart, use_container_width=True)

    habits = (
        data.groupby(["consome_alcool_nome", "fumante_nome"], as_index=False)
        .agg(media_horas=("horas_absenteismo", "mean"), registros=("id_colaborador", "size"))
    )
    habits["hábitos"] = (
        "Álcool: "
        + habits["consome_alcool_nome"]
        + " | Fumante: "
        + habits["fumante_nome"]
    )
    habit_chart = px.bar(
        habits,
        x="hábitos",
        y="media_horas",
        labels={"hábitos": "Perfil", "media_horas": "Média de horas"},
        title="Média de horas por hábitos sociais",
        color="media_horas",
        color_continuous_scale="Oranges",
    )
    habit_chart.update_layout(showlegend=False, coloraxis_showscale=False)
    right.plotly_chart(habit_chart, use_container_width=True)

    numeric = data.select_dtypes("number").rename(
        columns={"horas_absenteismo": "horas_absenteismo"}
    )
    correlations = (
        numeric.corr(numeric_only=True)["horas_absenteismo"]
        .drop("horas_absenteismo")
        .sort_values()
        .reset_index()
    )
    correlations.columns = ["variavel", "correlacao"]
    corr_chart = px.bar(
        correlations,
        x="correlacao",
        y="variavel",
        orientation="h",
        range_x=[-1, 1],
        labels={"variavel": "Variável", "correlacao": "Correlação"},
        title="Correlação com horas de absenteísmo",
        color="correlacao",
        color_continuous_scale="RdBu",
    )
    corr_chart.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(corr_chart, use_container_width=True)


def render_data(data: pd.DataFrame) -> None:
    st.subheader("Dados analíticos")
    st.caption("A tabela abaixo representa a camada detalhada usada para as visualizações.")
    columns = [
        "id_colaborador",
        "motivo_ausencia",
        "mes_nome",
        "estacao_nome",
        "idade",
        "distancia_casa_trabalho",
        "imc",
        "consome_alcool_nome",
        "fumante_nome",
        "horas_absenteismo",
    ]
    st.dataframe(
        data[columns].rename(
            columns={
                "id_colaborador": "Colaborador",
                "motivo_ausencia": "Motivo",
                "mes_nome": "Mês",
                "estacao_nome": "Estação",
                "idade": "Idade",
                "distancia_casa_trabalho": "Distância (km)",
                "imc": "IMC",
                "consome_alcool_nome": "Consome álcool",
                "fumante_nome": "Fumante",
                "horas_absenteismo": "Horas",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def main() -> None:
    st.set_page_config(
        page_title="Painel de Absenteísmo",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        """
        <style>
        .block-container { padding-top: 2rem; }
        [data-testid="stMetric"] {
            border: 1px solid #dbeafe;
            border-radius: 10px;
            padding: 12px;
            background: #f8fbff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    data = load_data()
    filtered = build_filters(data)

    st.title("Painel de Absenteísmo no Trabalho")
    st.markdown(
        "Monitoramento exploratório para apoiar decisões de gestão de pessoas, "
        "saúde ocupacional e produtividade."
    )
    st.caption(
        "Fonte: UCI Machine Learning Repository — Absenteeism at Work | "
        f"{len(data):,} registros carregados".replace(",", ".")
    )

    tabs = st.tabs(["Visão geral", "Perfil", "Fatores", "Dados"])
    with tabs[0]:
        render_overview(filtered)
    with tabs[1]:
        render_profile(filtered)
    with tabs[2]:
        render_factors(filtered)
    with tabs[3]:
        render_data(filtered)


if __name__ == "__main__":
    main()
