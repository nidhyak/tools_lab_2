$TTL 1d
$ORIGIN sender.com.

@       IN      SOA     ns1     root    (
                1               ;Serial
                12h             ;Refresh
                15m             ;Retry
                3w              ;Expire
                2h              ;Minimum
        )

@       IN      A       10.0.2.7

@       IN      NS      ns1
ns1     IN      A       10.0.2.7

@       IN      NS      ns2.sender.com.
ns2     IN      A       127.0.0.2

@       IN      MX      10      mail
mail    IN      A       10.0.2.7

www     IN      A       10.0.2.7

@       IN      TXT     "v=spf1 ip4:10.0.2.7 -all"

;VALID
default._domainkey IN TXT ("v=DKIM1;h=sha256;k=rsa;p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvWQL2VqOiT/7bI7nDIJG/IAjRb9bx603b249CpxoolCIKLh6zWabZQYdCbo8kci4rPr1AoC7vTUnFHT1PcSLKA6UpRqe2+2hn9jiDf/3mlXMeKSxUZXAM9jlI71dDp0rlgYwavix1LPrd6VoxR2uhkDw2FKDZDxNH9BVDohQtbDb4zlSsBwz6" "ufZ1kPelFkohtiYLulTFKC662CKIaYVSnklXHhl+ie9n68qHlcXvd6ssbm7Am2k85p3aJGQVJ79gK9bFJdBiHZjrU5V+3+gB7hRIKNG69sAv4ggEGKj1SNtPRULhNeXrH963MRQzP5Gw+8t/iejXoJYxE9dqodXGQIDAQAB")

;INVALID
;default._domainkey IN TXT ("v=DKIM1;h=sha256;k=rsa;p=THIS+IS+AN+INVALID+KEY+FAAOCAQ8AMIIBCgKCAQEAvWQL2VqOiT/7bI7nDIJG/IAjRb9bx603b249CpxoolCIKLh6zWabZQYdCbo8kci4rPr1AoC7vTUnFHT1PcSLKA6UpRqe2+2hn9jiDf/3mlXMeKSxUZXAM9jlI71dDp0rlgYwavix1LPrd6VoxR2uhkDw2FKDZDxNH9BVDohQtbDb4zlSsBwz6" "ufZ1kPelFkohtiYLulTFKC662CKIaYVSnklXHhl+ie9n68qHlcXvd6ssbm7Am2k85p3aJGQVJ79gK9bFJdBiHZjrU5V+3+gB7hRIKNG69sAv4ggEGKj1SNtPRULhNeXrH963MRQzP5Gw+8t/iejXoJYxE9dqodXGQIDAQAB")
