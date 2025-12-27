from typing import Optional, List
from app.services.decode_trips import TripDecoder
from app.services.routing_client import find_route
from app.services.format_output import format_server_journeys_for_user_llm
from app.graph.state import AgentState
from app.graph.nodes.format import format_node



route_response = {
  "num_journeys": 50,
  "journeys": [
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "APpubImR-DQ7ipx8VqTDi-07:00:00"
      ],
      "costs": {
        "money": 47.25,
        "transport_time": 704.0,
        "walk": 2457.545770895136
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "QyDZF4yDNAntbYpYmjfxj-07:00:00"
      ],
      "costs": {
        "money": 47.25,
        "transport_time": 693.0,
        "walk": 2457.545770895136
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "ZBtB-FXg8HG9MZ8swYNuQ-07:00:00"
      ],
      "costs": {
        "money": 47.25,
        "transport_time": 696.0,
        "walk": 2457.545770895136
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "aL3IoFC8Ob46ci80-r5J_-07:00:00"
      ],
      "costs": {
        "money": 47.25,
        "transport_time": 695.0,
        "walk": 2457.545770895136
      }
    },
    {
      "path": [
        "oL-cc2-4cc5VXM7r-ShUc-07:00:00",
        "APpubImR-DQ7ipx8VqTDi-07:00:00"
      ],
      "costs": {
        "money": 47.25,
        "transport_time": 690.0,
        "walk": 2457.545770895136
      }
    },
    {
      "path": [
        "oL-cc2-4cc5VXM7r-ShUc-07:00:00",
        "QyDZF4yDNAntbYpYmjfxj-07:00:00"
      ],
      "costs": {
        "money": 47.25,
        "transport_time": 679.0,
        "walk": 2457.545770895136
      }
    },
    {
      "path": [
        "oL-cc2-4cc5VXM7r-ShUc-07:00:00",
        "ZBtB-FXg8HG9MZ8swYNuQ-07:00:00"
      ],
      "costs": {
        "money": 47.25,
        "transport_time": 682.0,
        "walk": 2457.545770895136
      }
    },
    {
      "path": [
        "oL-cc2-4cc5VXM7r-ShUc-07:00:00",
        "aL3IoFC8Ob46ci80-r5J_-07:00:00"
      ],
      "costs": {
        "money": 47.25,
        "transport_time": 681.0,
        "walk": 2457.545770895136
      }
    },
    {
      "path": [
        "H4Zrbg3RLebdgA2rD0SL4-07:00:00",
        "APpubImR-DQ7ipx8VqTDi-07:00:00"
      ],
      "costs": {
        "money": 47.25,
        "transport_time": -173.0,
        "walk": 2462.7039566671233
      }
    },
    {
      "path": [
        "H4Zrbg3RLebdgA2rD0SL4-07:00:00",
        "QyDZF4yDNAntbYpYmjfxj-07:00:00"
      ],
      "costs": {
        "money": 47.25,
        "transport_time": -184.0,
        "walk": 2462.7039566671233
      }
    },
    {
      "path": [
        "H4Zrbg3RLebdgA2rD0SL4-07:00:00",
        "ZBtB-FXg8HG9MZ8swYNuQ-07:00:00"
      ],
      "costs": {
        "money": 47.25,
        "transport_time": -181.0,
        "walk": 2462.7039566671233
      }
    },
    {
      "path": [
        "H4Zrbg3RLebdgA2rD0SL4-07:00:00",
        "aL3IoFC8Ob46ci80-r5J_-07:00:00"
      ],
      "costs": {
        "money": 47.25,
        "transport_time": -182.0,
        "walk": 2462.7039566671233
      }
    },
    {
      "path": [
        "tL1NRyqKwJOCmUECmIQqO-07:00:00",
        "Rr5VrNghCMV3A0qeyJoVf-07:00:00",
        "1pTTdCYNksTHRhSFGpg76-07:00:00"
      ],
      "costs": {
        "money": 76.0,
        "transport_time": 1041.0,
        "walk": 1168.2628370508446
      }
    },
    {
      "path": [
        "tL1NRyqKwJOCmUECmIQqO-07:00:00",
        "Rr5VrNghCMV3A0qeyJoVf-07:00:00",
        "3SynmEGmJSDoBYRTRgEkj-07:00:00"
      ],
      "costs": {
        "money": 77.0,
        "transport_time": 658.0,
        "walk": 8241.462116628218
      }
    },
    {
      "path": [
        "tL1NRyqKwJOCmUECmIQqO-07:00:00",
        "Rr5VrNghCMV3A0qeyJoVf-07:00:00",
        "nnllgPNq1yuc-OXURFNAG-07:00:00"
      ],
      "costs": {
        "money": 76.0,
        "transport_time": 1043.0,
        "walk": 1168.2628370508446
      }
    },
    {
      "path": [
        "tL1NRyqKwJOCmUECmIQqO-07:00:00",
        "wNQ0rq7CAxb57IWuH3MiT-07:00:00",
        "mL3nX7_Swe2eUme5B7Ufy-07:00:00"
      ],
      "costs": {
        "money": 78.0,
        "transport_time": 662.0,
        "walk": 1188.1233701182891
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "4dazyxD50LYtjM4jq9_Ot-07:00:00",
        "Wq0wtD2-ddsT-JtVfCc3g-07:00:00"
      ],
      "costs": {
        "money": 88.5,
        "transport_time": 1834.0,
        "walk": 1586.0793317696437
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "3RevHK5a3aJRhrnXG0U-Y-07:00:00",
        "Wq0wtD2-ddsT-JtVfCc3g-07:00:00"
      ],
      "costs": {
        "money": 80.25,
        "transport_time": -884.0,
        "walk": 1559.0494172463968
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "APpubImR-DQ7ipx8VqTDi-07:00:00",
        "fZK7Eo97quKfWNkbl9oTR-07:00:00"
      ],
      "costs": {
        "money": 65.0,
        "transport_time": 654.0,
        "walk": 2483.410327643282
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "DQG7BcWUYPP3fo9nY8SBc-07:00:00",
        "APpubImR-DQ7ipx8VqTDi-07:00:00"
      ],
      "costs": {
        "money": 81.25,
        "transport_time": 1094.0,
        "walk": 1498.2810973622222
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "DQG7BcWUYPP3fo9nY8SBc-07:00:00",
        "QyDZF4yDNAntbYpYmjfxj-07:00:00"
      ],
      "costs": {
        "money": 81.25,
        "transport_time": 1074.0,
        "walk": 1498.2810973622222
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "DQG7BcWUYPP3fo9nY8SBc-07:00:00",
        "ZBtB-FXg8HG9MZ8swYNuQ-07:00:00"
      ],
      "costs": {
        "money": 81.25,
        "transport_time": 1070.0,
        "walk": 1498.2810973622222
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "KmoDyTTsPPrzF7JK4J700-07:00:00",
        "Wq0wtD2-ddsT-JtVfCc3g-07:00:00"
      ],
      "costs": {
        "money": 87.5,
        "transport_time": 1915.0,
        "walk": 1529.365446336978
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "KmoDyTTsPPrzF7JK4J700-07:00:00",
        "iUaEgr0LK4VOSZFkdzur6-07:00:00"
      ],
      "costs": {
        "money": 87.0,
        "transport_time": 3359.0,
        "walk": 3510.9429621423474
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "QyDZF4yDNAntbYpYmjfxj-07:00:00",
        "fZK7Eo97quKfWNkbl9oTR-07:00:00"
      ],
      "costs": {
        "money": 65.0,
        "transport_time": 650.0,
        "walk": 2483.410327643282
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "aL3IoFC8Ob46ci80-r5J_-07:00:00",
        "Wq0wtD2-ddsT-JtVfCc3g-07:00:00"
      ],
      "costs": {
        "money": 47.25,
        "transport_time": 695.0,
        "walk": 2572.179298217381
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "aL3IoFC8Ob46ci80-r5J_-07:00:00",
        "rz-CFcB9J3xy60VYWjZAn-07:00:00"
      ],
      "costs": {
        "money": 68.75,
        "transport_time": 889.0,
        "walk": 2096.9972259471047
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "iHxp5k-_O7q56ncOSt9aW-07:00:00",
        "QyDZF4yDNAntbYpYmjfxj-07:00:00"
      ],
      "costs": {
        "money": 92.75,
        "transport_time": 975.0,
        "walk": 1297.8858615081801
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "iHxp5k-_O7q56ncOSt9aW-07:00:00",
        "ZBtB-FXg8HG9MZ8swYNuQ-07:00:00"
      ],
      "costs": {
        "money": 93.0,
        "transport_time": -341.0,
        "walk": 1297.8858615081801
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "K1fkkoXPyuSsmQKdjzWHd-07:00:00",
        "mL3nX7_Swe2eUme5B7Ufy-07:00:00"
      ],
      "costs": {
        "money": 87.0,
        "transport_time": 413.0,
        "walk": 3336.780140974672
      }
    },
    {
      "path": [
        "FUo5FExiKwUTpyTUJYA7R-07:00:00",
        "WWP7DCP2cjGJxPZSN68Y2-07:00:00",
        "mL3nX7_Swe2eUme5B7Ufy-07:00:00"
      ],
      "costs": {
        "money": 86.0,
        "transport_time": 347.0,
        "walk": 3336.780140974672
      }
    },
    {
      "path": [
        "oL-cc2-4cc5VXM7r-ShUc-07:00:00",
        "PyvMsU4izplRo5xNtmlK3-07:00:00",
        "gp93eQ2WYNnUOJrA17bFP-07:00:00"
      ],
      "costs": {
        "money": 77.0,
        "transport_time": 3063.0,
        "walk": 1494.0470658233169
      }
    },
    {
      "path": [
        "oL-cc2-4cc5VXM7r-ShUc-07:00:00",
        "PyvMsU4izplRo5xNtmlK3-07:00:00",
        "gqntW1mb4ahLW_IHlR39R-07:00:00"
      ],
      "costs": {
        "money": 77.0,
        "transport_time": 3078.0,
        "walk": 1053.4807059242385
      }
    },
    {
      "path": [
        "oL-cc2-4cc5VXM7r-ShUc-07:00:00",
        "WWP7DCP2cjGJxPZSN68Y2-07:00:00",
        "mL3nX7_Swe2eUme5B7Ufy-07:00:00"
      ],
      "costs": {
        "money": 85.5,
        "transport_time": 311.0,
        "walk": 3336.780140974672
      }
    },
    {
      "path": [
        "oL-cc2-4cc5VXM7r-ShUc-07:00:00",
        "APpubImR-DQ7ipx8VqTDi-07:00:00",
        "fZK7Eo97quKfWNkbl9oTR-07:00:00"
      ],
      "costs": {
        "money": 65.0,
        "transport_time": 640.0,
        "walk": 2483.410327643282
      }
    },
    {
      "path": [
        "oL-cc2-4cc5VXM7r-ShUc-07:00:00",
        "QyDZF4yDNAntbYpYmjfxj-07:00:00",
        "fZK7Eo97quKfWNkbl9oTR-07:00:00"
      ],
      "costs": {
        "money": 65.0,
        "transport_time": 636.0,
        "walk": 2483.410327643282
      }
    },
    {
      "path": [
        "oL-cc2-4cc5VXM7r-ShUc-07:00:00",
        "aL3IoFC8Ob46ci80-r5J_-07:00:00",
        "rz-CFcB9J3xy60VYWjZAn-07:00:00"
      ],
      "costs": {
        "money": 68.75,
        "transport_time": 875.0,
        "walk": 2096.9972259471047
      }
    },
    {
      "path": [
        "oL-cc2-4cc5VXM7r-ShUc-07:00:00",
        "vGWP0NAWQ2WwsR_DTpmn9-07:00:00",
        "PAh8O-96IhPU2mfK1XGjm-07:00:00"
      ],
      "costs": {
        "money": 85.75,
        "transport_time": 1517.0,
        "walk": 1728.0990747238557
      }
    },
    {
      "path": [
        "oL-cc2-4cc5VXM7r-ShUc-07:00:00",
        "vGWP0NAWQ2WwsR_DTpmn9-07:00:00",
        "_npHlyCCY7o0R20RyqvT8-07:00:00"
      ],
      "costs": {
        "money": 86.0,
        "transport_time": 1286.0,
        "walk": 1728.0990747238557
      }
    },
    {
      "path": [
        "oL-cc2-4cc5VXM7r-ShUc-07:00:00",
        "vGWP0NAWQ2WwsR_DTpmn9-07:00:00",
        "gp93eQ2WYNnUOJrA17bFP-07:00:00"
      ],
      "costs": {
        "money": 85.5,
        "transport_time": 1288.0,
        "walk": 1529.165088752893
      }
    },
    {
      "path": [
        "oL-cc2-4cc5VXM7r-ShUc-07:00:00",
        "vGWP0NAWQ2WwsR_DTpmn9-07:00:00",
        "gqntW1mb4ahLW_IHlR39R-07:00:00"
      ],
      "costs": {
        "money": 86.0,
        "transport_time": 1596.0,
        "walk": 1287.5327148247773
      }
    },
    {
      "path": [
        "z8pSD1wGRKg4oVh4eC0Iw-07:00:00",
        "M-k1V2EbMTbdd6jCLeoZw-07:00:00",
        "3SynmEGmJSDoBYRTRgEkj-07:00:00"
      ],
      "costs": {
        "money": 78.25,
        "transport_time": 160.0,
        "walk": 1711.2247677515204
      }
    },
    {
      "path": [
        "z8pSD1wGRKg4oVh4eC0Iw-07:00:00",
        "M-k1V2EbMTbdd6jCLeoZw-07:00:00",
        "EglZxh1NkJA5Jax303ARy-07:00:00"
      ],
      "costs": {
        "money": 78.25,
        "transport_time": 110.0,
        "walk": 1267.4949023942202
      }
    },
    {
      "path": [
        "z8pSD1wGRKg4oVh4eC0Iw-07:00:00",
        "M-k1V2EbMTbdd6jCLeoZw-07:00:00",
        "PAh8O-96IhPU2mfK1XGjm-07:00:00"
      ],
      "costs": {
        "money": 78.5,
        "transport_time": 3364.0,
        "walk": 1659.048394036418
      }
    },
    {
      "path": [
        "z8pSD1wGRKg4oVh4eC0Iw-07:00:00",
        "M-k1V2EbMTbdd6jCLeoZw-07:00:00",
        "_npHlyCCY7o0R20RyqvT8-07:00:00"
      ],
      "costs": {
        "money": 78.75,
        "transport_time": 3133.0,
        "walk": 1659.048394036418
      }
    },
    {
      "path": [
        "z8pSD1wGRKg4oVh4eC0Iw-07:00:00",
        "M-k1V2EbMTbdd6jCLeoZw-07:00:00",
        "rz-CFcB9J3xy60VYWjZAn-07:00:00"
      ],
      "costs": {
        "money": 78.25,
        "transport_time": 64.0,
        "walk": 1267.4949023942202
      }
    },
    {
      "path": [
        "H4Zrbg3RLebdgA2rD0SL4-07:00:00",
        "APpubImR-DQ7ipx8VqTDi-07:00:00",
        "fZK7Eo97quKfWNkbl9oTR-07:00:00"
      ],
      "costs": {
        "money": 65.0,
        "transport_time": -223.0,
        "walk": 2488.5685134152695
      }
    },
    {
      "path": [
        "H4Zrbg3RLebdgA2rD0SL4-07:00:00",
        "QyDZF4yDNAntbYpYmjfxj-07:00:00",
        "fZK7Eo97quKfWNkbl9oTR-07:00:00"
      ],
      "costs": {
        "money": 65.0,
        "transport_time": -227.0,
        "walk": 2488.5685134152695
      }
    },
    {
      "path": [
        "H4Zrbg3RLebdgA2rD0SL4-07:00:00",
        "aL3IoFC8Ob46ci80-r5J_-07:00:00",
        "Wq0wtD2-ddsT-JtVfCc3g-07:00:00"
      ],
      "costs": {
        "money": 47.25,
        "transport_time": -182.0,
        "walk": 2577.3374839893686
      }
    },
    {
      "path": [
        "H4Zrbg3RLebdgA2rD0SL4-07:00:00",
        "aL3IoFC8Ob46ci80-r5J_-07:00:00",
        "rz-CFcB9J3xy60VYWjZAn-07:00:00"
      ],
      "costs": {
        "money": 68.75,
        "transport_time": 12.0,
        "walk": 2102.155411719092
      }
    }
  ],
  "start_trips_found": 5,
  "end_trips_found": 19
}
# decoder = TripDecoder()
# filtered_journeys = decoder.filter_sort(route_response)

# for journey in filtered_journeys:
#     path_ids = journey.get("path", [])
#     readable_path = decoder.decode_path(path_ids)
#     print(" → ".join(readable_path))

# new_state = format_node(state)
# print("\n===== FINAL ANSWER =====\n")
# print(new_state["final_answer"])
# print("\n=======================\n")

# assert "final_answer" in new_state

origin = "فلمنج"
destination = "عزبة سعد"

decoder = TripDecoder()

# 2️⃣ فلترة وترتيب
best_journeys = decoder.filter_sort(route_response)

# 3️⃣ decoding
for j in best_journeys:
    j["readable_path"] = decoder.decode_path(j.get("path", []))

# 4️⃣ فورمات باستخدام LLM
final_text = format_server_journeys_for_user_llm(
    journeys=best_journeys,
    origin=origin,
    dest=destination
)

print("\n========== FINAL OUTPUT ==========\n")
print(final_text)
print("\n=================================\n")