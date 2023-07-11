# coding: utf-8
# command: sqlacodegen postgresql://postgres:postgres@0.0.0.0:5450/postgres --outfile db_models.py
from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, String, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Enum


Base = declarative_base()
metadata = Base.metadata


class Discipline(Base):
    __tablename__ = 'disciplines'

    dis_id = Column(Integer, primary_key=True, server_default=text("nextval('dis_seq'::regclass)"))
    name = Column(String(500), nullable=False, unique=True, comment='Название дисциплины')


class Division(Base):
    __tablename__ = 'divisions'
    __table_args__ = (
        CheckConstraint("(chair)::text = ANY (ARRAY[('y'::character varying)::text, ('n'::character varying)::text])"),
        CheckConstraint("(faculty)::text = ANY (ARRAY[('y'::character varying)::text, ('n'::character varying)::text])")
    )

    div_id = Column(Integer, primary_key=True)
    name = Column(String(500), nullable=False, unique=True, comment='название подразделения')
    short = Column(String(255), nullable=False)
    faculty = Column(String(1), nullable=False, server_default=text("'n'::character varying"), comment='является факультетом')
    chair = Column(String(1), nullable=False, server_default=text("'n'::character varying"), comment='является кафедрой')
    div_div_id = Column(ForeignKey('divisions.div_id'), index=True)

    div_div = relationship('Division', remote_side=[div_id])


class EduForm(Base):
    __tablename__ = 'edu_forms'

    efo_id = Column(Integer, primary_key=True)
    name = Column(String(500), nullable=False, unique=True, comment='Название формы обучения')
    short = Column(String(3), nullable=False, unique=True, comment='Краткое обозначение')


class EduLevel(Base):
    __tablename__ = 'edu_levels'

    ele_id = Column(Integer, primary_key=True)
    name = Column(String(500), nullable=False, unique=True, comment='Название')
    short = Column(String(5), unique=True, comment='Краткое обозначение')
    srt = Column(Integer, comment='Сортировка')


class ExamType(Base):
    __tablename__ = 'exam_type'

    ext_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True, comment='название типа контроля (экзамен, зачёт)')
    short = Column(String(20), nullable=False, unique=True, comment='краткое обозначение')


class NrGroup(Base):
    __tablename__ = 'nr_groups'

    ngr_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)


class StuGroup(Base):
    __tablename__ = 'stu_groups'

    sgr_id = Column(Integer, primary_key=True, server_default=text("nextval('stu_seq'::regclass)"))
    name = Column(String(500), nullable=False, unique=True, comment='Имя группы')
    dgr_id = Column(Integer, comment='DIS_GROUPS из ЕТИС')
    info = Column(String(1000), comment='Комментарий')
    sgr_sgr_id = Column(ForeignKey('stu_groups.sgr_id'), index=True)

    sgr_sgr = relationship('StuGroup', remote_side=[sgr_id])


class TeachProgType(Base):
    __tablename__ = 'teach_prog_types'

    tpt_id = Column(Integer, primary_key=True)
    tp_type = Column(String(255), nullable=False, comment='Тип учебной программы')
    type_info = Column(String(240), comment='Краткое описание')


class TeachYear(Base):
    __tablename__ = 'teach_years'

    ty_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True, comment='название (напр. "2002-2003")')
    start_date = Column(Date, nullable=False, unique=True, comment='дата начала учебного года')
    end_date = Column(Date, nullable=False, comment='дата оканчания учебного года')


class Version(Base):
    __tablename__ = 'versions'

    ver_id = Column(Integer, primary_key=True, server_default=text("nextval('ver_seq'::regclass)"))
    calc_date = Column(Date, nullable=False, unique=True, comment='дата расчета')
    info = Column(String(4000), comment='описание')


class WorkType(Base):
    __tablename__ = 'work_types'

    wot_id = Column(Integer, primary_key=True)
    name = Column(String(500), nullable=False, unique=True, comment='Название')
    short = Column(String(255), nullable=False, comment='Короткое название')
    aud = Column(String(3), comment='Включать в аудиторные часы?')
    include_in_tpd = Column(String(3), comment='доступен ли для включения в учебную программу?')
    oneday = Column(String(1), nullable=False, server_default=text("'n'::character varying"), comment='Вся работа в один день')
    srt = Column(Integer, comment='Порядок сортировки')


class GroupFaculty(Base):
    __tablename__ = 'group_faculties'
    __table_args__ = (
        UniqueConstraint('ele_ele_id', 'efo_efo_id', 'sgr_sgr_id', 'div_div_id', 'num_course'),
    )

    grf_id = Column(Integer, primary_key=True, server_default=text("nextval('gr_fclt_seq'::regclass)"))
    stu_count = Column(Integer, nullable=False, comment='Количество студентов')
    num_course = Column(Integer, nullable=False, comment='Номер курса')
    ele_ele_id = Column(ForeignKey('edu_levels.ele_id'), nullable=False, index=True)
    efo_efo_id = Column(ForeignKey('edu_forms.efo_id'), nullable=False, index=True)
    div_div_id = Column(ForeignKey('divisions.div_id'), nullable=False, index=True)
    sgr_sgr_id = Column(ForeignKey('stu_groups.sgr_id'), nullable=False, index=True)

    div_div = relationship('Division')
    efo_efo = relationship('EduForm')
    ele_ele = relationship('EduLevel')
    sgr_sgr = relationship('StuGroup')


class GroupJoint(Base):
    __tablename__ = 'group_joints'
    __table_args__ = (
        UniqueConstraint('ngr_ngr_id', 'sgr_sgr_id'),
    )

    grj_id = Column(Integer, primary_key=True)
    sgr_sgr_id = Column(ForeignKey('stu_groups.sgr_id'), nullable=False, index=True)
    ngr_ngr_id = Column(ForeignKey('nr_groups.ngr_id'), nullable=False, index=True)

    ngr_ngr = relationship('NrGroup')
    sgr_sgr = relationship('StuGroup')


class GroupWork(Base):
    __tablename__ = 'group_works'
    __table_args__ = (
        UniqueConstraint('sgr_sgr_id', 'wt_wot_id'),
    )

    grw_id = Column(Integer, primary_key=True, server_default=text("nextval('gr_work_seq'::regclass)"))
    sgr_sgr_id = Column(ForeignKey('stu_groups.sgr_id'), nullable=False, index=True)
    wt_wot_id = Column(ForeignKey('work_types.wot_id'), nullable=False, index=True)

    sgr_sgr = relationship('StuGroup')
    wt_wot = relationship('WorkType')


class TeachProgram(Base):
    __tablename__ = 'teach_programs'

    tpr_id = Column(Integer, primary_key=True)
    confirm_date = Column(Date, comment='дата утверждения')
    status = Column(String(1), nullable=False, comment='статус программы дисциплины')
    protocol = Column(String(255), comment='номер протокола')
    practice_form = Column(String(255), comment='сопособ проведения практики (стационарная, выездная)')
    practice_schedule = Column(String(25), comment='вид проведения практики по отношению к графику (непрерывная, дискретная)')
    info = Column(String(4000), comment='предназначение')
    dis_dis_id = Column(ForeignKey('disciplines.dis_id'), nullable=False, index=True)
    tpt_tpt_id = Column(ForeignKey('teach_prog_types.tpt_id'), nullable=False, index=True)

    dis_dis = relationship('Discipline', lazy="joined")
    tpt_tpt = relationship('TeachProgType', lazy="joined")

    def __repr__(self):
        return f"<TeachProgram: tpr_id={self.tpr_id}, confirm_date={self.confirm_date}, status={self.status}, protocol={self.protocol} " \
               f"practice_form={self.practice_form}, practice_schedule={self.practice_schedule}, info={self.info}, " \
               f"dis_dis_id={self.dis_dis_id}, tpt_tpt_id={self.tpt_tpt_id}, dis_dis={self.dis_dis}, tpt_tpt={self.tpt_tpt} >"


class TwForYear(Base):
    __tablename__ = 'tw_for_years'

    twfy_id = Column(Integer, primary_key=True, server_default=text("nextval('tw_for_year_seq'::regclass)"))
    ty_ty_id = Column(ForeignKey('teach_years.ty_id'), nullable=False, index=True)
    wt_wot_id = Column(ForeignKey('work_types.wot_id'), nullable=False, index=True)

    ty_ty = relationship('TeachYear')
    wt_wot = relationship('WorkType')


class TyPeriod(Base):
    __tablename__ = 'ty_periods'
    __table_args__ = (
        UniqueConstraint('ty_ty_id', 'num'),
    )

    typ_id = Column(Integer, primary_key=True)
    num = Column(Integer, nullable=False, comment='Номер триместра')
    start_date = Column(Date, comment='Начало учебного периода по унифицированному графику')
    end_date = Column(Date, comment='Конец учебного периода по унифицированному графику')
    period_type = Column(String(255), nullable=False, comment='название учебного периода (триместр и семестр)')
    ty_ty_id = Column(ForeignKey('teach_years.ty_id'), nullable=False, index=True)

    ty_ty = relationship('TeachYear')


class TimeRule(Base):
    __tablename__ = 'time_rules'

    tr_id = Column(Integer, primary_key=True, server_default=text("nextval('time_rule_seq'::regclass)"))
    text = Column(String(1000), nullable=False, comment='Текстовая формулировка')
    info = Column(String(1000), comment='Примечания')
    value = Column(Integer, nullable=False, comment='Значение нормы')
    degree = Column(Integer, comment='Порядок, степень 10, на который умножается VALUE')
    prorate_ctrl_cnt = Column(Enum('y', 'n'), nullable=False, server_default='n', comment='Пропорционально количеству точек контроля раздела')
    prorate_tc_val = Column(Enum('y', 'n'), nullable=False, server_default='n', comment='Пропорционально общей нагрузке отдела')
    prorate_tc_eval = Column(Enum('y', 'n'), nullable=False, server_default='n', comment='Пропорционально зачтенным часам')
    prorate_tc_aud = Column(Enum('y', 'n'), nullable=False, server_default='n', comment='Пропорционально аудиторной нагрузке раздела')
    prorate_st_cnt = Column(Enum('y', 'n'), nullable=False, server_default='n', comment='Пропорционально количеству судентов')
    norm_ctrl_cnt = Column(Enum('y', 'n'), nullable=False, server_default='n', comment='Нормировать к суммарному количеству точек контроля')
    norm_tpr_val = Column(Enum('y', 'n'), nullable=False, server_default='n', comment='Нормировать к суммарной нагрузке УМК')
    forward_aud_toe = Column(Enum('y', 'n'), nullable=False, server_default='n', comment='Отчетность в следующих по ауд нагрузке в семестрах')
    tgc_rec_cnt = Column(Integer, comment='Количество записей нормы при раздаче нагрузки')
    tr_tr_id = Column(Integer)
    tpt_tpt_id = Column(ForeignKey('teach_prog_types.tpt_id'), index=True)
    ver_ver_id = Column(ForeignKey('versions.ver_id'), nullable=False, index=True)
    ext_ext_id = Column(ForeignKey('exam_type.ext_id'), index=True)
    twfy_twfy_id = Column(ForeignKey('tw_for_years.twfy_id'), nullable=False, index=True)
    wt_wot_id = Column(ForeignKey('work_types.wot_id'), index=True)

    ext_ext = relationship('ExamType')
    tpt_tpt = relationship('TeachProgType')
    twfy_twfy = relationship('TwForYear')
    ver_ver = relationship('Version')
    wt_wot = relationship('WorkType')


class TpDelivery(Base):
    __tablename__ = 'tp_deliveries'
    __table_args__ = (
        UniqueConstraint('name', 'tpr_tpr_id'),
    )

    tpdl_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    tpr_tpr_id = Column(ForeignKey('teach_programs.tpr_id'), nullable=False, index=True)

    tpr_tpr = relationship('TeachProgram')


class TprChapter(Base):
    __tablename__ = 'tpr_chapters'

    tch_id = Column(Integer, primary_key=True, server_default=text("nextval('tpr_seq'::regclass)"))
    name = Column(String(500), nullable=False, comment='Название раздела')
    srt = Column(Integer, nullable=False, comment='Порядок сортировки')
    info = Column(String(1000), comment='Комментарий')
    ext_ext_id = Column(ForeignKey('exam_type.ext_id'), index=True)
    tpdl_tpdl_id = Column(ForeignKey('tp_deliveries.tpdl_id'), nullable=False, index=True)
    tc_id = Column(Integer)

    ext_ext = relationship('ExamType')
    tpdl_tpdl = relationship('TpDelivery')


class DgrPeriod(Base):
    __tablename__ = 'dgr_periods'
    __table_args__ = (
        UniqueConstraint('div_div_id', 'sgr_sgr_id', 'typ_typ_id', 'ver_ver_id', 'tch_tch_id'),
    )

    dgp_id = Column(Integer, primary_key=True, server_default=text("nextval('dgr_seq'::regclass)"))
    tch_tch_id = Column(ForeignKey('tpr_chapters.tch_id'), nullable=False, index=True)
    ver_ver_id = Column(ForeignKey('versions.ver_id'), nullable=False, index=True)
    sgr_sgr_id = Column(ForeignKey('stu_groups.sgr_id'), nullable=False, index=True)
    typ_typ_id = Column(ForeignKey('ty_periods.typ_id'), nullable=False, index=True)
    div_div_id = Column(ForeignKey('divisions.div_id'), nullable=False, index=True)

    div_div = relationship('Division')
    sgr_sgr = relationship('StuGroup')
    tch_tch = relationship('TprChapter')
    typ_typ = relationship('TyPeriod')
    ver_ver = relationship('Version')


class TcTime(Base):
    __tablename__ = 'tc_times'
    __table_args__ = (
        UniqueConstraint('wt_wot_id', 'tch_tch_id'),
    )

    tim_id = Column(Integer, primary_key=True, server_default=text("nextval('tc_seq'::regclass)"))
    val = Column(Integer, nullable=False, comment='трудоёмкость (объём работы) в часах')
    ctl_count = Column(Integer, nullable=False, comment='количество точек контроля')
    wt_wot_id = Column(ForeignKey('work_types.wot_id'), nullable=False, index=True)
    tch_tch_id = Column(ForeignKey('tpr_chapters.tch_id'), nullable=False, index=True)
    totc_id = Column(Integer)

    tch_tch = relationship('TprChapter')
    wt_wot = relationship('WorkType')


class TwBlock(Base):
    __tablename__ = 'tw_blocks'
    __table_args__ = (
        UniqueConstraint('dgp_dgp_id', 'wt_wot_id', 'wt_wot_id_initialized_by'),
    )

    twb_id = Column(Integer, primary_key=True, server_default=text("nextval('tw_block_seq'::regclass)"))
    val = Column(Integer, nullable=False, comment='размер работы в часах астрономические')
    conv_value = Column(Integer, nullable=False, comment='размер в общепринятых часы')
    wt_wot_id = Column(ForeignKey('work_types.wot_id'), nullable=False, index=True)
    dgp_dgp_id = Column(ForeignKey('dgr_periods.dgp_id'), nullable=False, index=True)
    wt_wot_id_initialized_by = Column(ForeignKey('work_types.wot_id'), index=True)

    dgp_dgp = relationship('DgrPeriod')
    wt_wot = relationship('WorkType', primaryjoin='TwBlock.wt_wot_id == WorkType.wot_id')
    work_type = relationship('WorkType', primaryjoin='TwBlock.wt_wot_id_initialized_by == WorkType.wot_id')
