package user.license

allowed_licenses := {
    "MIT",
}

deny[msg] {
    lic := input.Licenses[_]
    
    not allowed_licenses[lic.Name]
    
    msg = sprintf(
        "未許可のライセンスを検出しました: %s (パッケージ: %s)。このライセンスはホワイトリストに含まれていないか、継承義務（GPL等）または商用制約がある可能性があります。", 
        [lic.Name, input.PkgName]
    )
}
