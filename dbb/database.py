# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from models.models import Base
SQLALCHEMY_DATABASE_URL = "sqlite:///./bank.db"


##Açıklama: create_engine fonksiyonu, SQLAlchemy veritabanı motorunu oluşturur.
##connect_args={"check_same_thread": False} argümanı, SQLite’ın aynı iş
##parçacığında çalışmasını kontrol eden bir ayardır. Bu, SQLite’ın aynı iş
##parçacığında çalışmasını zorunlu kılmamak için kullanılır.

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


##Açıklama: sessionmaker fonksiyonu, veritabanı oturumlarını oluşturmak için bir
##yapılandırıcı döner. autocommit=False ve autoflush=False ayarları, oturumların
##otomatik olarak commit ve flush yapmamasını sağlar. bind=engine argümanı,
##oturumların hangi veritabanı motoruna bağlanacağını belirtir.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



#Base = declarative_base()


##get_db fonksiyonu, veritabanı oturumlarını yönetmek için bir jeneratör
##fonksiyonudur. SessionLocal() ile yeni bir oturum oluşturur. yield db ifadesi,
##oturumu döner ve finally bloğunda oturumu kapatır. Bu, oturumların güvenli
##bir şekilde açılıp kapatılmasını sağlar.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
connect_args={"check_same_thread": False} argümanı, SQLite veritabanı
bağlantısının aynı iş parçacığında çalışmasını zorunlu kılmamak için kullanılır. Bu ayarın ne anlama geldiğini ve neden kullanıldığını daha iyi anlamak için iş parçacığı kavramını ve SQLite’ın çalışma prensiplerini açıklayalım:

İş Parçacığı (Thread)
Açıklama: İş parçacığı, bir programın aynı anda birden fazla işlemi
gerçekleştirebilmesini sağlayan en küçük işlem birimidir. Birden fazla
iş parçacığı, aynı anda çalışarak programın performansını artırabilir.

SQLite ve İş Parçacıkları
Açıklama: SQLite, varsayılan olarak aynı iş parçacığında çalışmayı zorunlu
kılar. Bu, bir SQLite bağlantısının yalnızca oluşturulduğu iş parçacığında
kullanılabileceği anlamına gelir. Bu kısıtlama, veri bütünlüğünü korumak ve
veri yarışmalarını önlemek için getirilmiştir.

check_same_thread Argümanı
Açıklama: check_same_thread argümanı, SQLite bağlantısının aynı iş parçacığında çalışıp çalışmayacağını belirler. False olarak ayarlandığında, SQLite bağlantısı farklı iş parçacıklarında kullanılabilir hale gelir. Bu, özellikle web uygulamaları gibi çok iş parçacıklı ortamlarda faydalıdır.

Neden Kullanılır?
Açıklama: FastAPI gibi çok iş parçacıklı web framework’lerinde, aynı veritabanı
bağlantısının farklı iş parçacıklarında kullanılabilmesi gerekebilir.
check_same_thread=False ayarı, bu durumu mümkün kılar ve veritabanı bağlantısının farklı iş parçacıklarında güvenli bir şekilde kullanılmasını sağlar.

Örnek Kullanım
Açıklama: Aşağıdaki örnek, check_same_thread=False ayarının nasıl kullanıldığını gösterir:
Python

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
Bu ayar, SQLite bağlantısının farklı iş parçacıklarında kullanılabilmesini
sağlar ve FastAPI gibi çok iş parçacıklı uygulamalarda veritabanı bağlantısının
güvenli bir şekilde yönetilmesine yardımcı olur"""
