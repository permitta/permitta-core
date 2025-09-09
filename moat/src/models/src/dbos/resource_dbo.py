from database import BaseModel
from models.src.dbos.common_mixin_dbo import IngestionDboMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship


class ResourceDbo(IngestionDboMixin, BaseModel):
    __tablename__ = "resources"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    fq_name: str = Column(String)
    platform: str = Column(String)
    object_type: str = Column(String)

    attributes: Mapped[list["ResourceAttributeDbo"]] = relationship(
        "ResourceAttributeDbo",
        primaryjoin="ResourceAttributeDbo.fq_name == ResourceDbo.fq_name",
        foreign_keys=fq_name,
        remote_side="ResourceAttributeDbo.fq_name",
        uselist=True,
    )


class ResourceAttributeDbo(IngestionDboMixin, BaseModel):
    __tablename__ = "resource_attributes"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    fq_name: str = Column(String)
    attribute_key: str = Column(String)
    attribute_value: str = Column(String)

    #  FK
    # resource_id: Mapped[int] = mapped_column(ForeignKey("resources.id"), nullable=True)
    # resource: Mapped["ResourceDbo"] = relationship(back_populates="attributes")
