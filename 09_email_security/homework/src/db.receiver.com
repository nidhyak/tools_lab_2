$TTL 1d
$ORIGIN receiver.com.

@       IN      SOA     ns1     root    (
                1               ;Serial
                12h             ;Refresh
                15m             ;Retry
                3w              ;Expire
                2h              ;Minimum
        )

@       IN      A       10.0.2.8

@       IN      NS      ns1
ns1     IN      A       10.0.2.8

@       IN      NS      ns2.receiver.com.
ns2     IN      A       127.0.0.2

@       IN      MX      10      mail
mail    IN      A       10.0.2.8

www     IN      A       10.0.2.8
