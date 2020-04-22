def main():
    import rsa
    from multiprocessing import cpu_count

    pubkey, privkey = rsa.newkeys(4096, True, cpu_count())

    with open(u"private.pem", "wb") as fl:
        fl.write(privkey.save_pkcs1())
    with open(u"public.pem", "wb") as fl:
        fl.write(pubkey.save_pkcs1())

    # We also create Python files in which we store the objects as variables, for faster access.
    with open(u"publickey.py", "w") as fl:
        fl.write("pk = {}".format(tuple(str(pubkey)[10:][:-1].split(", "))))
    with open(u"privatekey.py", "w") as fl:
        fl.write("pk = {}".format(tuple(str(privkey)[11:][:-1].split(", "))))

if __name__ == '__main__':
    main()
