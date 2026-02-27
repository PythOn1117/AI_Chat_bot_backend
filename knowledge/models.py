from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


# 网络资产模型
class NetworkAsset(Base):
    __tablename__ = 'network_assets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    resource_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(200))
    type = Column(String(100))
    model = Column(String(100))
    manufacturer = Column(String(100))
    creator = Column(String(100))
    picture = Column(String(500))
    height_m = Column(Float)
    longitude = Column(Float)
    latitude = Column(Float)
    department = Column(String(200))
    description = Column(Text)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    source = Column(String(100))
    spec = Column(JSON)


# 硬件模型
class Hardware(Base):
    __tablename__ = 'hardware'

    id = Column(Integer, primary_key=True, autoincrement=True)
    resource_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(200))
    type = Column(String(100))
    description = Column(Text)
    cpu_model = Column(String(200))
    architecture = Column(String(50))
    core_count = Column(Integer)
    memory_gb = Column(Float)
    storage_gb = Column(Integer)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    spec = Column(JSON)


# 软件模型
class Software(Base):
    __tablename__ = 'software'

    id = Column(Integer, primary_key=True, autoincrement=True)
    resource_id = Column(String(100), unique=True, nullable=False)
    pid = Column(Integer)
    name = Column(String(200))
    type = Column(String(100))
    description = Column(Text)
    port = Column(JSON)  # List[Integer]
    os_type = Column(String(100))
    kernel_version = Column(String(100))
    version = Column(String(100))
    spec = Column(JSON)


# 能力模型
class Capability(Base):
    __tablename__ = 'capabilities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    resource_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(200))
    description = Column(String(500))
    instruction_name = Column(String(200))
    instruction_params = Column(JSON)
    type = Column(String(100))  # 可用节点类型


# 漏洞模型
class Vulnerability(Base):
    __tablename__ = 'vulnerabilities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    resource_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(200))
    cve_id = Column(String(50))
    description = Column(Text)
    cvss_3_score = Column(Float)
    source = Column(String(100))
    level = Column(String(50))  # 风险等级


# 物理实体模型
class PhysicalEntity(Base):
    __tablename__ = 'physical_entities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    resource_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(200))
    type = Column(String(100))
    model = Column(String(100))
    manufacturer = Column(String(100))
    creator = Column(String(100))
    picture = Column(String(500))
    description = Column(String(500))
    length_m = Column(Float)
    width_m = Column(Float)
    height_m = Column(Float)
    longitude = Column(Float)
    latitude = Column(Float)
    max_weight_kg = Column(Float)
    max_height_m = Column(Float)
    max_range_km = Column(Float)  # 修正了拼写错误
    max_speed_kmh = Column(Float)
    direction = Column(Float)
    weapons = Column(JSON)
    status = Column(String(100))
    spec = Column(JSON)


# 网络链路模型
class NetworkLink(Base):
    __tablename__ = 'network_links'

    id = Column(Integer, primary_key=True, autoincrement=True)
    resource_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(200))
    link_type = Column(String(100))
    link_subtype = Column(String(100))
    description = Column(String(500))
    physical_medium = Column(String(100))
    connector_type = Column(String(100))
    length_m = Column(Float)
    theoretical_max_mbps = Column(Integer)
    available_mbps = Column(Integer)
    distance = Column(Float)
    interference = Column(JSON)
    spec = Column(JSON)


# 流量模型
class Traffic(Base):
    __tablename__ = 'traffic'

    id = Column(Integer, primary_key=True, autoincrement=True)
    resource_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(200))
    type = Column(String(100))
    description = Column(String(500))
    packet_count = Column(Integer)
    total_bytes = Column(Integer)
    duration = Column(Integer)
    source_ip = Column(String(50))
    destination_ip = Column(String(50))
    protocol = Column(String(50))
    source_port = Column(Integer)
    destination_port = Column(Integer)
    avg_packet_size = Column(Float)
    packets_per_second = Column(Float)
    start_time_offset_ms = Column(Integer)
    loop_count = Column(Integer)
    spec = Column(JSON)


# 实例表（综合表）
class Instance(Base):
    __tablename__ = 'instances'

    # 基础信息
    id = Column(Integer, primary_key=True, autoincrement=True)
    resource_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(200))
    type = Column(String(100))
    sub_type = Column(String(100))
    template_id = Column(String(100))
    model = Column(String(100))
    manufacturer = Column(String(100))
    creator = Column(String(100))
    picture = Column(String(500))
    status = Column(String(100))
    department = Column(String(200))
    description = Column(Text)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    source = Column(String(100))

    # 计算/硬件信息
    cpu_model = Column(String(200))
    architecture = Column(String(50))
    core_count = Column(Integer)
    memory_gb = Column(Float)
    storage_gb = Column(Integer)
    software_info = Column(JSON)
    vul_info = Column(JSON)
    interface = Column(JSON)
    security_policies = Column(JSON)
    nat_policies = Column(JSON)
    route_tables = Column(JSON)
    ports = Column(JSON)

    # 物理/空间信息
    length_m = Column(Float)
    width_m = Column(Float)
    height_m = Column(Float)
    longitude = Column(Float)
    latitude = Column(Float)
    max_weight_kg = Column(Float)
    max_height_m = Column(Float)
    max_range_km = Column(Float)  # 修正了拼写错误
    max_speed_kmh = Column(Float)
    direction = Column(Float)
    weapons = Column(JSON)

    # 网络/链路信息
    theoretical_max_mbps = Column(Integer)
    available_mbps = Column(Integer)
    distance = Column(Float)
    traffic_data = Column(JSON)
    left_node = Column(String(100))
    right_node = Column(String(100))
    node_id = Column(String(100))


# 关联表定义
# 网络资产模型-硬件模型关联表
class NetworkAssetHardware(Base):
    __tablename__ = 'network_asset_hardware'

    id = Column(Integer, primary_key=True, autoincrement=True)
    net_asset_id = Column(String(100), ForeignKey('network_assets.resource_id'))
    hardware_id = Column(String(100), ForeignKey('hardware.resource_id'))


# 网络资产模型-软件模型关联表
class NetworkAssetSoftware(Base):
    __tablename__ = 'network_asset_software'

    id = Column(Integer, primary_key=True, autoincrement=True)
    net_asset_id = Column(String(100), ForeignKey('network_assets.resource_id'))
    software_id = Column(String(100), ForeignKey('software.resource_id'))


# 网络资产模型-能力模型关联表
class NetworkAssetCapability(Base):
    __tablename__ = 'network_asset_capability'

    id = Column(Integer, primary_key=True, autoincrement=True)
    net_asset_id = Column(String(100), ForeignKey('network_assets.resource_id'))
    capability_id = Column(String(100), ForeignKey('capabilities.resource_id'))


# 硬件模型-漏洞模型关联表
class HardwareVulnerability(Base):
    __tablename__ = 'hardware_vulnerability'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hardware_id = Column(String(100), ForeignKey('hardware.resource_id'))
    vul_id = Column(String(100), ForeignKey('vulnerabilities.resource_id'))


# 软件模型-漏洞模型关联表
class SoftwareVulnerability(Base):
    __tablename__ = 'software_vulnerability'

    id = Column(Integer, primary_key=True, autoincrement=True)
    software_id = Column(String(100), ForeignKey('software.resource_id'))
    vul_id = Column(String(100), ForeignKey('vulnerabilities.resource_id'))


# 物理实体模型-网络资产模型关联表
class PhysicalEntityNetworkAsset(Base):
    __tablename__ = 'physical_entity_network_asset'

    id = Column(Integer, primary_key=True, autoincrement=True)
    net_asset_id = Column(String(100), ForeignKey('network_assets.resource_id'))
    physical_id = Column(String(100), ForeignKey('physical_entities.resource_id'))


# 物理实体模型-能力模型关联表
class PhysicalEntityCapability(Base):
    __tablename__ = 'physical_entity_capability'

    id = Column(Integer, primary_key=True, autoincrement=True)
    physical_id = Column(String(100), ForeignKey('physical_entities.resource_id'))
    capability_id = Column(String(100), ForeignKey('capabilities.resource_id'))


# 可选：添加关系定义到主模型
NetworkAsset.hardware = relationship("NetworkAssetHardware", backref="network_asset")
NetworkAsset.software = relationship("NetworkAssetSoftware", backref="network_asset")
NetworkAsset.capabilities = relationship("NetworkAssetCapability", backref="network_asset")
NetworkAsset.physical_entities = relationship("PhysicalEntityNetworkAsset", backref="network_asset")

Hardware.network_assets = relationship("NetworkAssetHardware", backref="hardware")
Hardware.vulnerabilities = relationship("HardwareVulnerability", backref="hardware")

Software.network_assets = relationship("NetworkAssetSoftware", backref="software")
Software.vulnerabilities = relationship("SoftwareVulnerability", backref="software")

Vulnerability.hardware = relationship("HardwareVulnerability", backref="vulnerability")
Vulnerability.software = relationship("SoftwareVulnerability", backref="vulnerability")

PhysicalEntity.network_assets = relationship("PhysicalEntityNetworkAsset", backref="physical_entity")
PhysicalEntity.capabilities = relationship("PhysicalEntityCapability", backref="physical_entity")

Capability.network_assets = relationship("NetworkAssetCapability", backref="capability")
Capability.physical_entities = relationship("PhysicalEntityCapability", backref="capability")