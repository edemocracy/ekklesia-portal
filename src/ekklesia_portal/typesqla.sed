s/ = integer_pk/: int = integer_pk/g
s/ = C(Integer/: int = C(Integer/g
s/ = C(Text/: str = C(Text/g
s/ = C(String(\[0-9\]\+)/: str = C(Text/g
s/ = C(String/: str = C(Text/g
s/ = C(DateTime/: datetime = C(DateTime/g
s/ = C(Date/: datetime = C(DateTime/g
s/ = C(Boolean/: bool = C(Boolean/g
s/ = Column(Integer/: int = C(Integer/g
s/ = Column(Text/: str = C(Text/g
s/ = Column(String(\[0-9\]\+)/: str = C(Text/g
s/ = Column(String/: str = C(Text/g
s/ = Column(DateTime/: datetime = C(DateTime/g
s/ = Column(Date/: datetime = C(DateTime/g
s/ = Column(Boolean/: bool = C(Boolean/g
s/ = Column(Enum(\(.\+\))/: \1 = C(Enum(\1)/g
