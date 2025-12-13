import sys, os, zipfile, json

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))

def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def load_yaml(p):
    import yaml

    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def schema_paths():
    return {
        "manifest": os.path.join(REPO, "schemas", "uapf-manifest.schema.json"),
        "enterprise": os.path.join(REPO, "schemas", "enterprise-index.schema.json"),
        "mapping": os.path.join(REPO, "schemas", "resource-mapping.schema.json"),
    }

def validate_package(path):
    from jsonschema import validate

    sp = schema_paths()
    m = load_yaml(os.path.join(path, "uapf.yaml"))
    validate(instance=m, schema=load_json(sp["manifest"]))

    # Level 4 structural checks
    if m.get("level") == 4:
        bpmn_dir = os.path.join(path, m.get("paths", {}).get("bpmn", "bpmn"))
        if not os.path.isdir(bpmn_dir):
            raise SystemExit("ERROR: Level 4 requires /bpmn directory")
        has_bpmn = any(fn.endswith(".bpmn.xml") for fn in os.listdir(bpmn_dir))
        if not has_bpmn:
            raise SystemExit("ERROR: Level 4 requires at least one *.bpmn.xml file")

        map_path = os.path.join(path, m.get("paths", {}).get("resources", "resources"), "mappings.yaml")
        if not os.path.isfile(map_path):
            raise SystemExit("ERROR: Level 4 requires resources/mappings.yaml")
        validate(instance=load_yaml(map_path), schema=load_json(sp["mapping"]))

def validate_enterprise_index(path):
    from jsonschema import validate

    sp = schema_paths()
    e = load_yaml(path)
    validate(instance=e, schema=load_json(sp["enterprise"]))

def pack(package_dir, out_file):
    with zipfile.ZipFile(out_file, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(package_dir):
            for f in files:
                fp = os.path.join(root, f)
                rel = os.path.relpath(fp, package_dir)
                z.write(fp, arcname=rel)

def unpack(in_file, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    with zipfile.ZipFile(in_file, "r") as z:
        z.extractall(out_dir)

def main():
    if len(sys.argv) < 3:
        print("Usage: uapf.py <validate|pack|unpack> <path> [out]")
        sys.exit(2)

    cmd = sys.argv[1]
    if cmd == "validate":
        p = sys.argv[2]
        if os.path.isdir(p) and os.path.isfile(os.path.join(p, "uapf.yaml")):
            validate_package(p)
            print("OK: package valid:", p)
        elif os.path.isfile(p) and p.endswith(".yaml"):
            validate_enterprise_index(p)
            print("OK: enterprise index valid:", p)
        else:
            raise SystemExit("ERROR: Provide a package directory (with uapf.yaml) or an enterprise.yaml")
    elif cmd == "pack":
        package_dir = sys.argv[2]
        out = sys.argv[3]
        pack(package_dir, out)
        print("OK: packed to", out)
    elif cmd == "unpack":
        inf = sys.argv[2]
        out = sys.argv[3]
        unpack(inf, out)
        print("OK: unpacked to", out)
    else:
        raise SystemExit("Unknown command: " + cmd)

if __name__ == "__main__":
    main()
