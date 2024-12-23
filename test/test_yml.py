import yaml

with open("result.yml", "r") as fp:
    dwe_data = yaml.safe_load(fp)
    print(dwe_data)