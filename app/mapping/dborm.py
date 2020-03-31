from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, Float, DateTime
from sqlalchemy import create_engine

Base = declarative_base()

class TSZAuth(Base):
    """
    CREATE TABLE `tsz_auth` (
        `uindex` int NOT NULL AUTO_INCREMENT ,
        `uid` int NOT NULL COMMENT '客户信息的唯一标识',
        `uname` varchar(50) CHARACTER SET utf8 NOT NULL COMMENT '客户的登录名(邮箱/手机号/别名) 均可 小于50字节',
        `uauthkey` varchar(50) CHARACTER SET utf8 NULL COMMENT '用户的登录密码,加密字符串',
        `udesc` text CHARACTER SET utf8 NULL,
        `uorgid` enum('0','1') NULL DEFAULT '0' COMMENT '权限设计，0普通权限 1管理员权限',
        `uemail` varchar(128) NULL,
        `utel` varchar(11) NULL,
         PRIMARY KEY (`uindex`)
    )COMMENT = '认证登录表';
    """
    __tablename__ = 'tsz_auth'
    __table_args__ = {'extend_existing': True}
    uid = Column(Integer, ForeignKey("tsz_user.user_id"), nullable=False, comment='客户的ID', primary_key=True)
    uname = Column(String(50), nullable=False, comment='客户的登录名(登录名/邮箱/电话号码)')
    uauthkey = Column(String(50), nullable=True, comment='客户加密的秘钥')
    udesc = Column(Text, comment='其他信息')
    uorgid = Column(Enum('0', '1'), default='0', comment='0: 普通权限 1:管理员权限')
    utel = Column(String(11), nullable=True, comment='电话号码')
    uemail = Column(String(128), nullable=True, comment='邮箱地址')

    def __repr__(self):
        return "<TSZAuth(uid='%d', uname='%s', uauthkey='%s')>" % (self.uid, self.uname, self.uauthkey)

class TSZUser(Base):
    """
    CREATE TABLE `tsz_user` (
        `user_id` int NOT NULL AUTO_INCREMENT COMMENT '客户的唯一标识ID 无重复',
        `user_orgid` enum('0','1') NULL DEFAULT '0' COMMENT '用户组权限， 0:普通人权限 1:管理员权限',
        `user_name` varchar(128) CHARACTER SET utf8 NOT NULL COMMENT '客户的名称',
        `user_nickname` varchar(128) CHARACTER SET utf8 NULL DEFAULT '' COMMENT '用户昵称',
        `user_university` varchar(255) NULL DEFAULT '' COMMENT '用户的所在大学',
        `user_age` int(3) check(user_age > 0 && user_age < 150),
        `user_email` varchar(128) CHARACTER SET utf8 NULL DEFAULT '' COMMENT '用户的邮箱地址',
        `user_phone` char(11) NULL COMMENT '用户电话',
        `user_sex` enum('0','1','2') NULL DEFAULT '0' COMMENT '用户性别 0:保密 1:男 2:女',
        `user_address` text NULL COMMENT '用户的默认地址',
        `user_icon` varchar(128) NULL DEFAULT '' COMMENT '用户的ICON地址 ',
        `user_locked` enum('0','1') NULL DEFAULT '0' COMMENT '0 标识正常客户， 1标识 锁定客户 ',
        `user_locked_reason` text NULL COMMENT '用户被锁定的原因',
        PRIMARY KEY (`user_id`)
    )COMMENT = '用户表';
    """
    __tablename__ = 'tsz_user'
    __table_args__ = {'extend_existing': True}
    user_id = Column(Integer, primary_key=True, autoincrement=True, comment='客户唯一标志ID')
    user_orgid = Column(Enum('0', '1'), default='0', comment='0: 普通权限 1:管理员权限')
    user_name = Column(String(128), nullable=True, comment='客户的登录名')
    user_nickname = Column(String(128), nullable=True, default='', comment='客户昵称')
    user_university = Column(String(256), nullable=True, default='', comment='客户学校名称')
    user_age = Column(Integer, default=18, comment='用户年龄')
    user_email = Column(String(128), nullable=True, comment='邮箱地址')
    user_phone = Column(String(11), nullable=True, comment='电话号码')
    user_address = Column(Text, comment='地址信息')
    user_icon = Column(String(128), comment='icon地址')
    user_locked = Column(Enum('0', '1'), default='0', comment='0:正常 1:锁定')
    user_locked_reason = Column(Text, comment='锁定原因')

    def __repr__(self):
        return "<TSZUser(user_id='%d', user_name='%s')>" % (self.user_id, self.user_name)

class TSZAddress(Base):
    """
    CREATE TABLE `tsz_address` (
        `addr_id` int NOT NULL AUTO_INCREMENT COMMENT '收信地址的ID',
        `addr_uid` int NOT NULL,
        `addr_name` varchar(20) NOT NULL COMMENT '地址的别名',
        `addr_country` varchar(50) CHARACTER SET utf8 NOT NULL COMMENT '地址对应的国家',
        `addr_iso_code` varchar(5) NOT NULL COMMENT '地址的ISOcode',
        `addr_province` varchar(50) NULL COMMENT '地址对应的省/直辖市/自治区/特别行政区',
        `addr_city` varchar(50) NULL COMMENT '地址的城市名(地级市/县/区)',
        `addr_detail` text CHARACTER SET utf8 NOT NULL COMMENT '详细地址信息',
        `addr_phone` varchar(20) NOT NULL COMMENT '地址对应的联系方式',
        PRIMARY KEY (`addr_id`)
    )ENGINE = MyISAM DEFAULT CHARACTER SET = utf8 COMMENT = '用户地址表';
    """
    __tablename__ = 'tsz_address'
    __table_args__ = {'extend_existing': True}
    addr_id = Column(Integer, autoincrement=True, primary_key=True, comment='地址序号')
    addr_uid = Column(Integer, ForeignKey("tsz_user.user_id"), comment='对应用户的ID')
    addr_name = Column(String(20), comment='地址别名')
    addr_country = Column(String(50), comment='地址所属国别')
    addr_iso_code = Column(String(5), comment='地址所属国别的ISO编号')
    addr_province = Column(String(50), comment='地址所属省份')
    addr_city = Column(String(50), comment='地址所属城市')
    addr_detail = Column(Text, comment='地址详细细节')
    addr_phone = Column(String(20), comment='地址绑定地址')
    addr_postcode = Column(String(10), comment='邮政编码')

    def __repr__(self):
        return "<TSZAddress(addr_id='%d', addr_name='%s')>" % (self.addr_id, self.addr_name)

class TSZBooks(Base):
    """
    CREATE TABLE `tsz_books` (
        `book_id` int NOT NULL AUTO_INCREMENT COMMENT '图书的唯一标识ID',
        `book_uid` int NOT NULL COMMENT '图书的拥有者',
        `book_img_url` varchar(128) NOT NULL COMMENT '图书的图片地址 基于跟/',
        `book_edition` int NULL COMMENT '图书的版次',
        `book_publisher` varchar(128) NULL COMMENT '图书的出版社',
        `book_name` varchar(100) NOT NULL COMMENT '图书名字',
        `book_author_chief` varchar(128) NULL COMMENT '图书的主要作者',
        `book_author_other` varchar(256) NULL DEFAULT '' COMMENT '图书次要作者 按照;分割',
        `book_price` float NOT NULL DEFAULT 0.00 COMMENT '图书书本售价',
        `book_desc` text NULL COMMENT '图书其他信息',
        `book_locked` enum('0','1') NULL DEFAULT '1' COMMENT '图书的是否可用 0 不可用 1可用',
        `book_locked_reason` text NULL COMMENT '图书锁定的原因',
        PRIMARY KEY (`book_id`)
    )COMMENT = '本表标识卖家的图书，以及图书的所有者的关系';
    """
    __tablename__ = 'tsz_books'
    __table_args__ = {'extend_existing': True}
    book_id = Column(Integer, autoincrement=True, primary_key=True, comment='图书的ID')
    book_uid = Column(Integer, ForeignKey("tsz_user.user_id"), comment='图书对应user的ID')
    book_img_url = Column(String(128), comment='图书图片URL')
    book_edition = Column(Integer, comment='图书版次')
    book_publisher = Column(String(128), comment='图书的出版社')
    book_name = Column(String(100), comment='图书名')
    book_author_chief = Column(String(128), comment='图书主要作者')
    book_author_other = Column(String(256), comment='图书次要作者')
    book_price = Column(Float, default=0.0, comment='图书单价')
    book_desc = Column(Text, comment='图书其他信息')
    book_locked = Column(Enum('0', '1'), default='0', comment='0:正常 1:锁定')
    book_locked_reason = Column(Text, comment='锁定原因')

    def __repr__(self):
        return "<TSZBooks(book_id='%d', book_name='%s')>" % (self.book_id, self.book_name)

class TSZStore(Base):
    """
    CREATE TABLE `tsz_store` (
        `store_id` int NOT NULL AUTO_INCREMENT COMMENT '书店的唯一ID',
        `store_user_id` int NOT NULL COMMENT '外键， 对应用户的ID',
        `store_name` varchar(128) NULL DEFAULT NULL COMMENT '书店名字',
        `store_opened_time` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '开店时间',
        `store_enabled` enum('0','1') NOT NULL DEFAULT '0' COMMENT '书店是否开启， 0未开启 1已开启',
        `store_desc` text NULL COMMENT '书店简介',
        `store_physical` enum('0','1') NULL DEFAULT '0' COMMENT '是否拥有实体书店 0:无 1:有',
        `store_physical_address` varchar(256) NULL DEFAULT NULL COMMENT '实体书店的地址',
        `store_locked` enum('0','1') NULL DEFAULT '0' COMMENT '书店是否被锁定 0:无锁定 1锁定',
        `store_locked_reason` text NULL COMMENT '锁定原因',
        PRIMARY KEY (`store_id`)
    )COMMENT = '书店表';
    """
    __tablename__ = 'tsz_store'
    __table_args__ = {'extend_existing': True}
    store_id = Column(Integer, primary_key=True, autoincrement=True, comment='书店的唯一ID')
    store_user_id = Column(Integer, ForeignKey("tsz_user.user_id"), comment='外键， 对应用户的ID')
    store_opened_time = Column(DateTime, nullable=False, comment='开店时间')
    store_enabled = Column(Enum('0', '1'), default='0', comment='书店是否开启， 0未开启 1已开启')
    store_desc = Column(Text, comment='书店简介')
    store_physical = Column(Enum('0', '1'), default='0', comment='是否拥有实体书店 0:无 1:有')
    store_physical_address = Column(String(256), comment='实体书店的地址')
    store_locked = Column(Enum('0', '1'), default='0', comment='书店是否被锁定 0:无锁定 1锁定')
    store_locked_reason = Column(Text, comment='锁定原因')
    store_name = Column(String(128), comment='书店名称')

    def __repr__(self):
        return "<TSZStore(store_id='%d', sotre_name='%s')>" % (self.store_id, self.store_name)

class TSZOrder(Base):
    """
    CREATE TABLE `tsz_order` (
        `order_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '订单唯一ID',
        `order_store_id` int(11) NOT NULL COMMENT '订单的对应的书店ID',
        `order_user_id` int(255) NOT NULL COMMENT '提交订单对应的购买方的ID',
        `order_book_id` int(11) NOT NULL COMMENT '订单书籍的ID',
        `order_book_price` double NOT NULL DEFAULT 0.00 COMMENT '订单单价',
        `order_book_count` int NOT NULL,
        `order_description` text NULL COMMENT '订单详情',
        `order_date` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '订单时间',
        `order_state` enum('0','1','2','3','4','5','6') NOT NULL DEFAULT '0' COMMENT '订单状态 0:等待买家付款 1:付款确认中 2:买家已付款 3:买家已发货 4:交易成功 5:交易关闭 6:退款中订单',
        `order_finish_date` datetime NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '订单完成时间',
        PRIMARY KEY (`order_id`)
    )COMMENT = '订单表';
    """
    __tablename__ = 'tsz_order'
    __table_args__ = {'extend_existing': True}
    order_id = Column(Integer, autoincrement=True, primary_key=True, comment='订单唯一ID')
    order_store_id = Column(Integer, ForeignKey("tsz_store.store_id"), comment='订单的对应的书店ID')
    order_user_id = Column(Integer, ForeignKey("tsz_user.user_id"), comment='提交订单对应的购买方的ID')
    order_book_id = Column(Integer, ForeignKey("tsz_books.book_id"), comment='订单书籍的ID')
    order_book_price = Column(Float, default=0.00, comment='订单单价')
    order_book_count = Column(Integer, comment='订单数量')
    order_description = Column(Text, comment='订单详情')
    order_date = Column(DateTime, comment='订单时间')
    order_state = Column(Enum('0', '1', '2', '3', '4', '5', '6'), default='0',
                         comment='订单状态 0:等待买家付款 1:付款确认中 2:买家已付款 3:买家已发货 4:交易成功 5:交易关闭 6:退款中订单')
    order_finish_date = Column(DateTime, comment='订单完成时间')

    def __repr__(self):
        return "<TSZOrder(order_id='%d')>" % self.order_id

class TSZUserBooks(Base):
    """
    CREATE TABLE `tsz_user_books` (
        `user_id` int NOT NULL,
        `book_id` int NULL,
        `book_count` int NULL DEFAULT 0 COMMENT '图书的量',
        `book_bought_price` double UNSIGNED NULL COMMENT '客户购买的时候的图书价格'
    )COMMENT = '用户的已经拥有的图书';
    """
    __tablename__ = 'tsz_user_books'
    __table_args__ = {'extend_existing': True}
    user_id = Column(Integer, ForeignKey("tsz_user.user_id"), primary_key=True, comment='')
    book_id = Column(Integer, ForeignKey("tsz_books.book_id"), primary_key=True, comment='')
    book_count = Column(Integer, default=1, comment='图书的量')
    book_bought_price = Column(Float,  comment='客户购买的时候的图书价格')

if __name__ == '__main__':
    engine = create_engine("mysql+pymysql://root:123456@192.168.0.105:3306/taoshuzhai?charset=utf8")
    Base.metadata.create_all(engine)
    user = TSZUser(user_name='xhou', user_nickname='hekiw ')
    t = TSZAuth(uid=123, uname='xhou', uauthkey='123456', udesc='', uorgid='1', utel='13833211231',
                uemail='xhou@pp.com')
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(engine)
    db_session = Session()
    db_session.add(user)
    db_session.commit()
    db_session.close()
