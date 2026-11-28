import unittest
import numpy as np
import pandas as pd
from equity_research import evaluate

class EquityTests(unittest.TestCase):
    def prices(self):
        dates = pd.bdate_range("2020-01-01", periods=40)
        return pd.DataFrame({"MSFT": 100*np.cumprod(1+np.linspace(-.01,.02,40)),
                             "SPY": 100*np.cumprod(np.repeat(1.001,40))}, index=dates)
    def test_no_future_leakage(self):
        p = self.prices()
        first = evaluate(p, train_size=10)
        p.iloc[-1,0] *= 2
        second = evaluate(p, train_size=10)
        pd.testing.assert_series_equal(first.historical_mean, second.historical_mean)
    def test_baseline(self):
        p = self.prices()
        out = evaluate(p, train_size=10)
        expected = p.MSFT.pct_change().iloc[1:11].mean()
        self.assertAlmostEqual(out.historical_mean.iloc[0], expected)
    def test_invalid_prices(self):
        p = self.prices()
        p.iloc[5,0] = 0
        with self.assertRaises(ValueError):
            evaluate(p, train_size=10)

    def test_nonfinite_prices_rejected(self):
        for value in (np.nan,np.inf,-np.inf):
            p=self.prices(); p.iloc[5,0]=value
            with self.assertRaises(ValueError): evaluate(p,train_size=10)

    def test_input_structure_rejected(self):
        for p in (pd.DataFrame(),self.prices().drop(columns='SPY'),self.prices().rename(columns={'SPY':'MSFT'})):
            with self.assertRaises(ValueError): evaluate(p,train_size=10)

    def test_invalid_dates_rejected(self):
        for p in (self.prices().iloc[::-1],self.prices().reset_index(drop=True)):
            with self.assertRaises(ValueError): evaluate(p,train_size=10)
        p=self.prices(); p.index=[p.index[0]]*len(p)
        with self.assertRaises(ValueError): evaluate(p,train_size=10)
        p=self.prices(); dates=p.index.to_list(); dates[0]=pd.NaT; p.index=pd.DatetimeIndex(dates)
        with self.assertRaises(ValueError): evaluate(p,train_size=10)

    def test_bad_training_window(self):
        for size in (0,-1,True,1.5,np.nan,np.inf):
            with self.assertRaises(ValueError): evaluate(self.prices(),train_size=size)

    def test_bad_costs(self):
        for cost in (-1,np.inf,np.nan,10000,True):
            with self.assertRaises(ValueError): evaluate(self.prices(),train_size=10,cost_bps=cost)

    def test_insufficient_history(self):
        with self.assertRaises(ValueError): evaluate(self.prices(),train_size=39)

    def test_future_changes_leave_earlier_outputs_unchanged(self):
        p=self.prices(); original=evaluate(p,train_size=10)
        p.iloc[25:]*=1.5
        changed=evaluate(p,train_size=10)
        pd.testing.assert_frame_equal(original.loc[:p.index[24]],changed.loc[:p.index[24]])

    def test_initial_fee_and_compounding(self):
        out=evaluate(self.prices(),train_size=30,cost_bps=10)
        self.assertEqual(out.turnover.iloc[0],1)
        self.assertAlmostEqual(out.strategy_net.iloc[0],.999*(1+out.actual.iloc[0])-1)

    def test_flat_prices_are_valid_and_remain_cash(self):
        out=evaluate(self.prices()*0+100,train_size=10)
        self.assertTrue((out.position==0).all())
        self.assertTrue((out.strategy_net==0).all())

    def test_benchmarks_share_evaluation_dates(self):
        out=evaluate(self.prices(),train_size=10)
        self.assertEqual(len(out),29)
        self.assertFalse(out.isna().any().any())
        self.assertEqual(out.index[0],self.prices().index[11])

    def test_offline_cli(self):
        import tempfile, subprocess, sys
        from pathlib import Path
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'synthetic.csv'; output=Path(folder)/'results.csv'
            self.prices().to_csv(source,index_label='Date')
            run=subprocess.run([sys.executable,'equity_research.py','--csv',str(source),'--start','2020-01-01','--end','2021-01-01','--train-size','10','--output',str(output)],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertEqual(len(pd.read_csv(output)),29)

if __name__ == "__main__":
    unittest.main()
