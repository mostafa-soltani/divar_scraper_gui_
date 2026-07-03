from core.services import stats


class Report:

    def report_final(self,topic,city,runtime):
        """
        print the final report
        """
        print("\n========== REPORT ==========")
        print(f"Topic      : {topic}")
        print(f"City       : {city}")
        print(f"Ads Found  : {stats.ads_found}")
        print(f"Ads Saved  : {stats.ads_saved}")
        print(
            f"Duplicates : "
            f"{stats.ads_found - stats.ads_saved}"
        )
        print(f"Runtime    : {runtime}")
        print("============================")

