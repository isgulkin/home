# [Прошивка роутера Xiaomi AX3200](https://openwrt.org/toh/xiaomi/ax3200)

Сначала скачиваем патчер

```shell
git clone https://github.com/openwrt-xiaomi/xmir-patcher.git
cd xmir-patcher
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x run.sh
./run.sh
```

После этого заходим на роутер с помощью `ssh` или `telnet`

```shell
ssh -v -oHostKeyAlgorithms=+ssh-rsa root@192.168.31.1
```

Проверяем какая версия у нашего роутера

```shell
dd if=/dev/mtd2 2>/dev/null | grep -cF " 2022 - "
dd if=/dev/mtd2 2>/dev/null | grep -cF "do_env_export"
dd if=/dev/mtd2 2>/dev/null | grep -cF "GigaDevice"
```

Если версия 0 (старая, у меня вот эта!!!):

```shell
nvram set ssh_en=1
nvram set uart_en=1
nvram set boot_wait=on
nvram set flag_boot_success=1
nvram set flag_try_sys1_failed=0
nvram set flag_try_sys2_failed=0
nvram commit
```

Если версия 1 (новая):

```shell
nvram set boot_fw1="run boot_rd_img;bootm"
nvram set flag_try_sys1_failed=8
nvram set flag_try_sys2_failed=8
nvram set flag_boot_rootfs=0
nvram set flag_boot_success=1
nvram set flag_last_success=1
nvram commit
```

После этого на роутере (будет дисконнект, надо заново подключиться, хост должен поменять на 192.168.1.1)

```shell
cd /tmp
wget http://downloads.openwrt.org/releases/23.05.5/targets/mediatek/mt7622/openwrt-23.05.5-mediatek-mt7622-xiaomi_redmi-router-ax6s-squashfs-factory.bin
mv openwrt-23.05.5-mediatek-mt7622-xiaomi_redmi-router-ax6s-squashfs-factory.bin factory.bin
mtd -r write factory.bin firmware
```

После этого я смог подключиться к роутеру только через кабель

Далее выполняем следующие команды

```shell
uci show wireless # просмотр конфигурации
wifi status       # проверка статуса wi-fi
uci set wireless.@wifi-device[0].disabled=0 # включаем wi-fi 2.4 ГГц
uci set wireless.@wifi-device[1].disabled=0 # включаем wi-fi 5 ГГц
uci set wireless.@wifi-iface[0].ssid='NetworkName' # имя сети wi-fi 2.4 ГГц
uci set wireless.@wifi-iface[0].ssid='NetworkName' # имя сети wi-fi 5 ГГц
uci set wireless.@wifi-iface[0].encryption='psk2' # метод шифрования WPA2
uci set wireless.@wifi-iface[1].encryption='psk2' # метод шифрования WPA2
uci set wireless.@wifi-iface[0].key='Password' # пароль для wi-fi 2.4 ГГц
uci set wireless.@wifi-iface[1].key='Password' # пароль для wi-fi 5 ГГц
uci commit wireless
wifi reload
```

Вообще можно разделить сети, если одна сеть, то устройство само будет определять, как далеко оно находится от роутура и
будет выбирать лучшую сеть, лучше наверно всё-таки делить сети

## Прошивка успешно закончена, теперь самое интересное, надо сделать точечную маршрутизацию через VPN
```shell
sh <(wget -O - https://raw.githubusercontent.com/itdoginfo/domain-routing-openwrt/master/getdomains-install.sh)
```

Запускаем скрипт, выбираем Sing-box (3 на момент написания данной инструкции)
Далее скачиваем `DNSCrypt-proxy2` (2 на момент записи)
Выбираем, что мы находимся в России (1 на момент записи)

Далее редактируем сам конфиг
```shell
:> /etc/sing-box/config.json && nano s
```
После чего вставляем вот такой конфиг
```json
{
  "log": {
    "level": "debug"
  },
  "inbounds": [
    {
      "type": "tun",
      "interface_name": "tun0",
      "domain_strategy": "ipv4_only",
      "inet4_address": "172.16.250.1/30",
      "auto_route": false,
      "strict_route": false,
      "sniff": true
    }
  ],
  "outbounds": [
    {
      "type": "vless",
      "server": "",
      "server_port": ,
      "uuid": "",
      "flow": "xtls-rprx-vision",
      "tls": {
        "enabled": true,
        "insecure": false,
        "server_name": "www.yandex.com",
        "utls": {
          "enabled": true,
          "fingerprint": "random"
        },
        "reality": {
          "enabled": true,
          "public_key": "",
          "short_id": ""
        }
      }
    }
  ],
  "route": {
    "auto_detect_interface": true
  }
```

После чего делаем
```shell
service sing-box start
service network restart
```

Всё успешно установлено

Для всего этого деяния нужен сервер, там установить [3-ui](https://github.com/MHSanaei/3x-ui)
Там сделать пользователя и поставить настройки

#############
# Важно сделать, чтобы не было кирпича
В веб-интерфейсе OpenWRT (http://192.168.1.1) переходим: `System` > `Startup`, далее - вкладка `Local Startup` и вставляем вот это:
```
# Put your custom commands here that should be executed once
# the system init finished. By default this file does nothing.

fw_setenv flag_try_sys1_failed 0
fw_setenv flag_try_sys2_failed 0

exit 0

```
После чего под ssh сделать 
```shell
reboot
```
#############

Если ноут стал кирпичом, то надо скачать на виндоус машину вот [это](https://4pda.to/stat/go?u=http%3A%2F%2Fbigota.miwifi.com%2Fxiaoqiang%2Ftools%2FMIWIFIRepairTool.x86.zip&e=114089118&f=https%3A%2F%2F4pda.to%2Fforum%2Findex.php%3Fshowtopic%3D1033757%26st%3D360%23entry114089118)
После чего скачать вот этот файл

