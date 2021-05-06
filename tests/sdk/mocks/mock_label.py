from spb.labels import Label

MOCK_LABEL_JSON = {
        "id": "0bf55703-af2b-451c-8c2f-b0503dfd1eeb",
        "projectId": "2ece675e-6341-4eb3-ab1d-656df394385a",
        "tags": [],
        "status": "SUBMITTED",
        "stats": [
            {
                "id": "8bd2eb51-f4f4-4e2a-b40f-29bbc3b3aee9",
                "name": "Box",
                "count": 1
            }
        ],
        "workAssignee": "mjlee@superb-ai.com",
        "labelType": "MAIN_LABEL",
        "workapp": "IMAGE_SIESTA",
        "relatedLabelMethod": "",
        "consensusStatus": "",
        "consistencyScore": 0,
        "dataId": "5640f15e-c443-4a73-9f4e-341982b8fc68",
        "dataset": "20",
        "dataKey": "000000000632.jpg",
        "dataUrl": "https://suite-asset.dev.superb-ai.com/apne2/tenants/mjlee/assets/5640f15e-c443-4a73-9f4e-341982b8fc68/image.jpg?Expires=1619515881&Signature=C0wjgY83XiUXbDpaBamvDxBias2J8aAT6yV3JZFBLwzBWaVIvVrF-Q9DV856831D8D4IiWvDyyF4Y1pKj4Q3F0xibj7zu8hjBBr58iul0qrnAEJ0JSplknapHLl7ynSCsifBYV0Rn1yXygKo2NEoa8TIkG4ThI7bMc7Qr-4O7CkpfHNj00VaKzjnMBHF3qnsNT3h7xg159ApRQ5O92htjq00Ndavddnv7qWPi99pDWtYNurCKJMwoqzynOfN7jsKfJR-CU4MIRaKmB47QVlBYoYbLPNpMA1II5wp3WyRZlGiBCrTWoJiuTknmCG~ECobG75vRVUe1O8d-8SQkPocEg__&Key-Pair-Id=APKAIBKPXKPWUNCICOBA",
        "result": {"objects":[{"id":"580fc8f7-090f-42b1-ba6e-211a2c3a4d4b","classId":"8bd2eb51-f4f4-4e2a-b40f-29bbc3b3aee9","className":"Box","annotationType":"box","annotation":{"coord":{"x":68,"y":98.5,"width":484,"height":541.5},"meta":{"zIndex":1}},"properties":[]}],"categories":{"properties":[],"frames":[]}},
        "infoReadPresignedUrl": "https://suite-civet-asset-dev-s3.s3-accelerate.amazonaws.com/tenants/mjlee/projects/2ece675e-6341-4eb3-ab1d-656df394385a/labels/0bf55703-af2b-451c-8c2f-b0503dfd1eeb/info.json?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA2AH3SIVR52JTIQMR%2F20210427%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20210427T083121Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0yIkYwRAIgO%2FHDBmbPHc%2B3BTT1o%2B%2F9UllFQhFOEWnxd4VdE4cVVBcCIAX%2BkxNKXLLMxjGGaACFjjJjS5OyWFq1tl8lvO8jLezbKsADCD0QARoMNjg3NzIyMzQ5OTIzIgwdZQCrRCvrrijr6fAqnQNLrq5GTWR2STt1ZX0lFuoIRIOpxe4HahyzpE9mj6KHxAzOcaxz8H4WOFZYbZvzOM2SMKJSqS4194GJ6XKQLc9U%2F4MgCsAld36Y0rvRyH0Yca4ebdHV3JnGsciSwk4lrijhFh8WACBu8eAlszaxhfdofDINV%2BGdN09MkENhxQY8GhW3JcoEaV59PWL%2BKtvel9%2FgmquzrOFuHEYTtaW6ZxnfSGDGpf16X4tnT5977IFpVwazWEcBsrVMEt1HUaZgRE9WdfxSDbuoOtHEjw1iqutrXJhQDQcOw4MdiiXTOpkFjY0gRFpss5ljAv8qtAupHWw8ZBiiluk4AwNmuySNLMhLK%2FOagXj4MpW5zl7GAzQID0d8ChIx%2F%2BsO79aQBoL7EDhUs1W2xtR%2BKAouekh0mZSEo9uPsIV2vNkWMNe8dNw1%2FVyhg8DV44iSOX%2F90EsGRkVspIJ%2BNe%2B4OHKY%2FzKmSMEcov6sJTiM7jOc3dYr6H8MKdm6om%2F0v9BPLPNYoTYQWzNX16FSCPBAvwI7N%2BeM313Dqlpp3crPftSZe08X7zDQiJ6EBjrsAbvNxBc1uCdIGGFki1qklxeYkdQuw2M0qzHNiAs%2BCfeYr3dUsIM1UnCoF9jDYfnmU1EqZsVFAdvXan%2FoaL7GLfJe80dtg5B7ra4sZKnXBoaxipyluQjeT%2BimmZCwq7vC3H3wekT9TtYf%2FnCnEvfl%2FU1jNz66hiVEhuaSZ5%2F7FrjAt%2BqWWnRE5hbx402mJEdnaRii6Ddqa1qDywaQuhflxQvE48MeijHWQAcrNqsHplFVoYbzFgVNYqf%2B9ncr3t8Pn1aKCTYDIsMokQZ4SHcNfzOTXRZ56hDZWTIrdJj4znVS3ZyB0KO7bqkrIpPX&X-Amz-Signature=aad18c74e81e9f8fbc778de41947fd67ee5e195d2d81504cdd0bdeaea413430e",
        "infoWritePresignedUrl": "https://suite-civet-asset-dev-s3.s3-accelerate.amazonaws.com/tenants/mjlee/projects/2ece675e-6341-4eb3-ab1d-656df394385a/labels/0bf55703-af2b-451c-8c2f-b0503dfd1eeb/info.json?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA2AH3SIVR52JTIQMR%2F20210427%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20210427T083121Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0yIkYwRAIgO%2FHDBmbPHc%2B3BTT1o%2B%2F9UllFQhFOEWnxd4VdE4cVVBcCIAX%2BkxNKXLLMxjGGaACFjjJjS5OyWFq1tl8lvO8jLezbKsADCD0QARoMNjg3NzIyMzQ5OTIzIgwdZQCrRCvrrijr6fAqnQNLrq5GTWR2STt1ZX0lFuoIRIOpxe4HahyzpE9mj6KHxAzOcaxz8H4WOFZYbZvzOM2SMKJSqS4194GJ6XKQLc9U%2F4MgCsAld36Y0rvRyH0Yca4ebdHV3JnGsciSwk4lrijhFh8WACBu8eAlszaxhfdofDINV%2BGdN09MkENhxQY8GhW3JcoEaV59PWL%2BKtvel9%2FgmquzrOFuHEYTtaW6ZxnfSGDGpf16X4tnT5977IFpVwazWEcBsrVMEt1HUaZgRE9WdfxSDbuoOtHEjw1iqutrXJhQDQcOw4MdiiXTOpkFjY0gRFpss5ljAv8qtAupHWw8ZBiiluk4AwNmuySNLMhLK%2FOagXj4MpW5zl7GAzQID0d8ChIx%2F%2BsO79aQBoL7EDhUs1W2xtR%2BKAouekh0mZSEo9uPsIV2vNkWMNe8dNw1%2FVyhg8DV44iSOX%2F90EsGRkVspIJ%2BNe%2B4OHKY%2FzKmSMEcov6sJTiM7jOc3dYr6H8MKdm6om%2F0v9BPLPNYoTYQWzNX16FSCPBAvwI7N%2BeM313Dqlpp3crPftSZe08X7zDQiJ6EBjrsAbvNxBc1uCdIGGFki1qklxeYkdQuw2M0qzHNiAs%2BCfeYr3dUsIM1UnCoF9jDYfnmU1EqZsVFAdvXan%2FoaL7GLfJe80dtg5B7ra4sZKnXBoaxipyluQjeT%2BimmZCwq7vC3H3wekT9TtYf%2FnCnEvfl%2FU1jNz66hiVEhuaSZ5%2F7FrjAt%2BqWWnRE5hbx402mJEdnaRii6Ddqa1qDywaQuhflxQvE48MeijHWQAcrNqsHplFVoYbzFgVNYqf%2B9ncr3t8Pn1aKCTYDIsMokQZ4SHcNfzOTXRZ56hDZWTIrdJj4znVS3ZyB0KO7bqkrIpPX&X-Amz-Signature=414b530ea6182366b8b49ab74ab3bc9043f0e2bd644fc5b6d22bac189092280a",
        "createdBy": "mjlee@superb-ai.com",
        "createdAt": "2021-04-16T02:51:59.917179Z",
        "lastUpdatedBy": "mjlee@superb-ai.com",
        "lastUpdatedAt": "2021-04-22T06:08:22.860474Z"
    }

MOCK_LABEL = Label(**MOCK_LABEL_JSON)